import json
import logging
import asyncio
from resources.notification_checker import (is_ready_to_notify,
                                            update_last_notifications)
import pydantic
from os import environ
from pydantic import ValidationError
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from firebase_admin import messaging
from external.Users import UsersService
from ..common.middleware import Middleware
from database.models.measurement import Measurement
from database.database import SQLAlchemyClient
from resources.rule_parser import apply_rules
from schemas.measurement import MeasurementReadingSchema
from resources.message_parser import parse_message
from exceptions.logger_messages import LoggerMessages
from exceptions.invalid_insertion import InvalidInsertionError
from exceptions.deviating_parameters import DeviatedParametersError
from exceptions.empty_package import EmptyPackageError
from exceptions.row_not_found import RowNotFoundError


Base = declarative_base(
    metadata=MetaData(
        schema=environ.get("POSTGRES_SCHEMA", "measurements_service")
        )
)
logger = logging.getLogger("rabbitmq_consumer")
dbUrl = environ.get("DATABASE_URL").replace("postgres://", "postgresql://", 1)
engine = create_engine(dbUrl, echo=True, future=True)
session = Session(engine)


class Consumer:
    def __init__(self, topic):
        self.__middleware = Middleware()
        self.__sqlAlchemyClient = SQLAlchemyClient()
        self.__users = UsersService()
        self.__last_measurements = {}
        self.__last_notifications = {}
        self.__topic = topic

    def run(self):
        self.__middleware.listen_on(self.__callback, self.__topic)
        self.__middleware.connect()
        self.__middleware.run()

    def obtain_device_plant(self, measurement_from_rabbit):
        try:
            dp = self.__sqlAlchemyClient.find_by_device_id(
                measurement_from_rabbit.id_device
            )
            logger.debug(LoggerMessages.ROW_FOUND.format("DEVICE_PLANT", dp))
            return dp
        except Exception as err:
            logger.error(f"{err} - {type(err)}")
            raise RowNotFoundError(measurement_from_rabbit.id_device,
                                   "DEVICE_PLANT")

    async def obtain_user(self, user_id):
        return await self.__users.get_user(user_id)

    def check_package(self, measurement: MeasurementReadingSchema):
        empty_values = []
        if measurement.temperature is None:
            empty_values.append("temperature")

        if measurement.watering is None:
            empty_values.append("watering")

        if measurement.light is None:
            empty_values.append("light")

        # Nuestro sensor no mide humedad del ambiente!
        if measurement.humidity is None and not measurement.id_device.\
                startswith("sensor_"):
            empty_values.append("humidity")

        if measurement.id_device is None:
            empty_values.append("id_device")

        if len(empty_values) > 0:
            raise EmptyPackageError(empty_values)

    def generate_notification_body(self, error):
        parameters = {
            'temperature': 'temperatura',
            'humidity': 'humedad',
            'light': 'luz',
            'watering': 'riego'
        }

        low_parameters = []
        high_parameters = []
        error_dict = error.parameters.dict()

        for param, value in error_dict.items():
            if value == 'lower':
                low_parameters.append(parameters.get(param, param))
            elif value == 'higher':
                high_parameters.append(parameters.get(param, param))

        low_msg = ", ".join(f"{param}" for param in low_parameters)
        high_msg = ", ".join(f"{param}" for param in high_parameters)

        if low_msg and high_msg:
            return (
                f"Los siguientes parámetros están bajos: {low_msg}. "
                f"Y los siguientes están altos: {high_msg}."
            )
        elif low_msg:
            return f"Los siguientes parámetros están bajos: {low_msg}."
        elif high_msg:
            return f"Los siguientes parámetros están altos: {high_msg}."

    async def send_notification(self,
                                id_user,
                                measurement: MeasurementReadingSchema,
                                error: DeviatedParametersError,
                                details):

        device_plant = self.obtain_device_plant(measurement)

        if not is_ready_to_notify(self.__last_notifications,
                                  device_plant.id_plant,
                                  measurement):
            return

        try:
            user = await self.obtain_user(device_plant.id_user)
            notification_body = self.generate_notification_body(error)
            if user.device_token is not None:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title="Estado de tu planta", body=notification_body
                    ),
                    token=user.device_token,
                )
                messaging.send(message)
                update_last_notifications(self.__last_notifications,
                                          device_plant,
                                          measurement,
                                          error)

            logger.info(LoggerMessages.USER_NOTIFIED.format(id_user))

        except Exception as e:
            logger.error(f"Error sending notification. Detail: {e}")
            pass

    def apply_rules(self, measurement: MeasurementReadingSchema, device_plant):
        deviated_parameters = apply_rules(measurement, device_plant.plant_type)
        if deviated_parameters.hasDeviations():
            raise DeviatedParametersError(deviated_parameters)

    def save_measurement(self, measurement_from_rabbit, device_plant):
        measurement_from_db = Measurement(
            id_plant=device_plant.id_plant,
            plant_type=device_plant.plant_type,
            time_stamp=measurement_from_rabbit.time_stamp,
            temperature=measurement_from_rabbit.temperature,
            humidity=measurement_from_rabbit.humidity,
            light=measurement_from_rabbit.light,
            watering=measurement_from_rabbit.watering,
        )
        try:
            self.__sqlAlchemyClient.add(measurement_from_db)

            logger.info(
                LoggerMessages.NEW_ROW_INSERTED.format(
                    "MEASUREMENT", measurement_from_db
                )
            )
        except Exception as err:
            logger.error(f"{err} - {type(err)}")
            self.__sqlAlchemyClient.rollback()
            raise InvalidInsertionError(measurement_from_rabbit,
                                        "MEAUSUREMENT")

    def __callback(self, client, userdata, msg):
        device_plant = None
        measurement, body = parse_message(self.__last_measurements, msg)
        if measurement is None:
            return

        try:
            logger.info(
                LoggerMessages.NEW_PACKAGE_RECEIVED
                .format(measurement.id_device)
            )
            logger.debug(LoggerMessages.PACKAGE_DETAIL.format(body))

            device_plant = self.obtain_device_plant(measurement)
            self.check_package(measurement)
            self.apply_rules(measurement, device_plant)
        except (
            pydantic.errors.PydanticUserError,
            ValidationError,
            json.JSONDecodeError,
        ) as err:
            logger.warn(LoggerMessages.INVALID_PACKAGE_RECEIVED)
            logger.debug(LoggerMessages.ERROR_DETAILS.format(err, body))
        except RowNotFoundError as err:
            logger.warn(
                LoggerMessages.ROW_NOT_FOUND.format(err.primary_key,
                                                    err.name_table)
            )
            logger.debug(LoggerMessages.ERROR_DETAILS.format(err, body))

            device_plant = None
        except EmptyPackageError as err:
            logger.warn(LoggerMessages.EMPTY_PACKAGE_RECEIVED)
            logger.debug(LoggerMessages.ERROR_DETAILS.format(err, body))

            measurement = None
        except DeviatedParametersError as err:
            logger.warn(LoggerMessages.DEVIATING_PARAMETERS)
            logger.debug(LoggerMessages.ERROR_DETAILS.format(err, body))

            asyncio.run(self.send_notification(device_plant.id_user,
                                               measurement,
                                               err, body))

        if device_plant is not None and measurement is not None:
            try:
                self.save_measurement(measurement, device_plant)
            except InvalidInsertionError as err:
                logger.error(LoggerMessages.INVALID_INSERTION)
                logger.debug(LoggerMessages.ERROR_DETAILS.format(err, body))
