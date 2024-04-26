import json
from exceptions.logger_messages import LoggerMessages
import pydantic
import logging
from exceptions.invalid_insertion import InvalidInsertionError
from exceptions.deviating_parameters import DeviatedParametersError
from exceptions.empty_package import EmptyPackageError
from exceptions.row_not_found import RowNotFoundError
from pydantic import ValidationError
from schemas.measurement import MeasurementReadingSchema
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from ..common.middleware import Middleware
from database.models.measurement import Measurement
from database.database import SQLAlchemyClient
from resources.parser import apply_rules
from os import environ
from firebase_admin import messaging

Base = declarative_base(
    metadata=MetaData(schema=environ.get("POSTGRES_SCHEMA", "measurements_service"))
)
logger = logging.getLogger("rabbitmq_consumer")
logging.getLogger("pika").setLevel(logging.WARNING)
dbUrl = environ.get("DATABASE_URL").replace("postgres://", "postgresql://", 1)
engine = create_engine(dbUrl, echo=True, future=True)
session = Session(engine)


class Consumer:
    def __init__(self, queue_name):
        self.__queue_name = queue_name
        self.__middleware = Middleware()
        self.__sqlAlchemyClient = SQLAlchemyClient()

    def run(self):
        self.__middleware.create_queue(self.__queue_name)
        self.__middleware.listen_on(self.__queue_name, self.__callback)

    def obtain_device_plant(self, measurement_from_rabbit):
        try:
            dp = self.__sqlAlchemyClient.find_by_device_id(
                measurement_from_rabbit.id_device
            )
            logger.info(LoggerMessages.ROW_FOUND.format("DEVICE_PLANT", dp))
            return dp
        except Exception as err:
            logger.error(f"{err} - {type(err)}")
            raise RowNotFoundError(measurement_from_rabbit.id_device, "DEVICE_PLANT")

    def check_package(self, measurement):
        empty_values = []
        if measurement.temperature is None:
            empty_values.append("temperature")

        if measurement.watering is None:
            empty_values.append("watering")

        if measurement.light is None:
            empty_values.append("light")

        if measurement.humidity is None:
            empty_values.append("humidity")

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

    def send_notification(self, id_user, measurement, error, details):
        print(f"details: {details}")
        print(f"measurement: {measurement}")
        print(f"error: {error}")

        notification_body = self.generate_notification_body(error)

        print(f"notif body: {notification_body}")

        try:
            if measurement.device_token is not None:
                message = messaging.Message(
                    notification=messaging.Notification(title="Estado de tu planta",
                                                        body=notification_body),
                    token=measurement.device_token)
                messaging.send(message)
            logger.info(LoggerMessages.USER_NOTIFIED.format(id_user))

        except Exception:
            pass

    def apply_rules(self, measurement,  device_plant):
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
            raise InvalidInsertionError(measurement_from_rabbit, "MEAUSUREMENT")

    def __callback(self, body):
        device_plant = None
        measurement = None

        try:
            measurement = MeasurementReadingSchema(**json.loads(body))
            logger.info(
                LoggerMessages.NEW_PACKAGE_RECEIVED.format(measurement.id_device)
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
                LoggerMessages.ROW_NOT_FOUND.format(err.primary_key, err.name_table)
            )
            logger.debug(LoggerMessages.ERROR_DETAILS.format(err, body))

            device_plant = None  # For not saving the measurement.
        except EmptyPackageError as err:
            logger.warn(LoggerMessages.EMPTY_PACKAGE_RECEIVED)
            logger.debug(LoggerMessages.ERROR_DETAILS.format(err, body))

            # self.send_notification(device_plant.id_user, measurement, err, body)

            measurement = None  # For not saving the measurement.
        except DeviatedParametersError as err:
            logger.warn(LoggerMessages.DEVIATING_PARAMETERS)
            logger.debug(LoggerMessages.ERROR_DETAILS.format(err, body))

            self.send_notification(device_plant.id_user, measurement, err, body)

        if device_plant is not None and measurement is not None:
            try:
                self.save_measurement(measurement, device_plant)
            except InvalidInsertionError as err:
                logger.error(LoggerMessages.INVALID_INSERTION)
                logger.debug(LoggerMessages.ERROR_DETAILS.format(err, body))
