import os
import json
import pydantic
import logging
from exceptions.invalid_insertion import InvalidInsertionError
from exceptions.deviating_parameters import DeviatingParameters
from exceptions.empty_package import EmptyPackageError
from exceptions.row_not_found import RowNotFoundError
from pydantic import ValidationError
from schemas.measurement_reading import MeasurementReadingSchema
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from ..common.middleware import Middleware
from database.models.measurement import Measurement
from database.database import SQLAlchemyClient

Base = declarative_base(metadata=MetaData(schema='dev'))

logger = logging.getLogger("rabbitmq_consumer")


dbUrl = os.environ.get("DATABASE_URL")
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
            dp = self.__sqlAlchemyClient.find_device_plant(
                measurement_from_rabbit.id_device)
            logger.info(f"action: device_plant encontrado|device_plant: {dp}")
            return dp
        except Exception as err:
            logger.error(f"{err} - {type(err)}")
            raise RowNotFoundError(measurement_from_rabbit.id_device, "DEVICE_PLANT")

    def check_package(self, measurement_from_rabbit):
        logger.info("TO DO - Step #2 from Ticket HAN-14")
        # raise EmptyPackageError(["temperature", "humidity"])

    def send_notification(self, id_user, message):
        logger.info(f"[ ID_USER: {id_user} ]")
        logger.info("TO DO - For Step #2 & Step #4 from Ticket HAN-14")

    def apply_rules(self, measurement_from_rabbit, device_plant):
        logger.info("TO DO - Step #3 from Ticket HAN-14")
        logger.info("TO DO - Step #4 from Ticket HAN-14")

        # ...This is an example, the exception can be much more personalized...
        # raise DeviatingParametersError(["temperature", "humidity"])
    def save_measurement(self, measurement_from_rabbit, device_plant):
        logger.info("TO DO - Step #5 from Ticket HAN-14")

        # Indentation fixed (4 spaces)
        measurement_from_db = Measurement(
            id_plant=device_plant.id_plant,
            plant_type=device_plant.plant_type,
            time_stamp=measurement_from_rabbit.time_stamp,
            temperature=measurement_from_rabbit.temperature,
            humidity=measurement_from_rabbit.humidity,
            light=measurement_from_rabbit.light,
            watering=measurement_from_rabbit.watering
        )
        try:
            self.__sqlAlchemyClient.add_new(measurement_from_db)

            # Line length reduced by breaking up the string
            logger.info(
                "action: registro agregado a la base de datos"
                f"|measurement: {measurement_from_db}"
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
                f"[ NEW PACKAGE RECEIVED FROM ID_DEVICE = {measurement.id_device} ]")
            logger.debug(f"[ PACKAGE: {body} ]")

            device_plant = self.obtain_device_plant(measurement)
            self.check_package(measurement)
            self.apply_rules(measurement, device_plant)
        except pydantic.errors.PydanticUserError as err:
            logger.warn("[ INVALID PACKAGE RECEIVED ]")
            logger.debug(f"[ ERROR ] [ DETAIL: {err} ] [ PACKAGE: {body} ]")
        except ValidationError as err:
            logger.warn("[ INVALID PACKAGE RECEIVED ]")
            logger.debug(f"[ ERROR ] [ DETAIL: {err} ] [ PACKAGE: {body} ]")
        except json.JSONDecodeError as err:
            logger.warn("[ INVALID PACKAGE RECEIVED ]")
            logger.debug(f"[ ERROR ] [ DETAIL: {err} ] [ PACKAGE: {body} ]")
        except RowNotFoundError as err:
            logger.warn(f"[ DEVICE PLANT WITH ID = {err.primary_key} NOT FOUND ]")
            logger.debug(f"[ ERROR ] [ DETAIL: {err} ] [ PACKAGE: {body} ]")

            device_plant = None  # For not saving the measurement.
        except EmptyPackageError as err:
            logger.warn("[ EMPTY PACKAGE RECEIVED ] [ READY TO SEND NOTIFICATION ]")
            logger.debug(f"[ ERROR ] [ DETAIL: {err} ] [ PACKAGE: {body} ]")

            self.send_notification(device_plant.id_user, err)

            measurement = None  # For not saving the measurement.
        except DeviatingParameters as err:
            logger.warn("[ DEVIATING PARAMETERS ] [ READY TO SEND NOTIFICATION ]")
            logger.debug(f"[ ERROR ] [ DETAIL: {err} ] [ PACKAGE: {body} ]")

            # TO DO - Ticket HAN-17 & Step #4 from Ticket HAN-14
            # parameters = err.parameters  # List of deviating parameters.
            self.send_notification(device_plant.id_user, err)

        if device_plant is not None and measurement is not None:
            try:
                self.save_measurement(measurement, device_plant)
            except InvalidInsertionError as err:
                logger.error("[ INVALID INSERTION ]")
                logger.debug(f"[ ERROR ] [ DETAIL: {err} ] [ PACKAGE: {body} ]")
