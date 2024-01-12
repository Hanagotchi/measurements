import os
import json
import logging
from exceptions.invalid_insertion import InvalidInsertion
from exceptions.deviating_parameters import DeviatingParameters
from exceptions.empty_package import EmptyPackageError
from exceptions.row_not_found import RowNotFoundError
from pydantic import ValidationError
from schemas.measurement_reading import MeasurementReadingSchema
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from ..common.middleware import Middleware

Base = declarative_base(metadata=MetaData(schema='dev'))

logger = logging.getLogger("rabbitmq_consumer")


class DevicePlant(Base):
    __tablename__ = "device_plant"
    id_device = Column(String(32), primary_key=True)
    id_plant = Column(Integer, nullable=False, unique=True)
    plant_type = Column(Integer, nullable=False)
    id_user = Column(Integer, nullable=False)

    def __init__(self, id_device, id_plant, plant_type, id_user):
        self.id_device = id_device
        self.id_plant = id_plant
        self.plant_type = plant_type
        self.id_user = id_user


dbUrl = os.environ.get("DATABASE_URL")
engine = create_engine(dbUrl, echo=True, future=True)
session = Session(engine)


def obtain_device_plant(measurement, session):
    logger.info("TO DO - Step #1 from Ticket HAN-14")
    # raise RowNotFoundError("123", "DEVICE_PLANT")

    # Mocked object
    return DevicePlant(id_device="123", id_plant=1, plant_type=1, id_user=1)


def check_package(measurement):
    logger.info("TO DO - Step #2 from Ticket HAN-14")
    # raise EmptyPackageError(["temperature", "humidity"])


def send_notification(id_user, message):
    logger.info(f"[ ID_USER: {id_user} ]")
    logger.info("TO DO - For Step #2 & Step #4 from Ticket HAN-14")


def apply_rules(measurement, device_plant):
    logger.info("TO DO - Step #3 from Ticket HAN-14")
    logger.info("TO DO - Step #4 from Ticket HAN-14")

    # ...This is an example, the exception can be much more personalized...
    # raise DeviatingParametersError(["temperature", "humidity"])


def save_measurement(measurement, device_plant, session):
    logger.info("TO DO - Step #5 from Ticket HAN-14")

    # ...Maybe there are more bugs in the sql library.
    # Wrap them all in a single exception as InvalidInsertion...
    # raise InvalidInsertionError(measurement, "MEASUREMENTS")


class Consumer:
    def __init__(self, queue_name):
        self.__queue_name = queue_name
        self.__middleware = Middleware()

    def run(self):
        self.__middleware.create_queue(self.__queue_name)
        self.__middleware.listen_on(self.__queue_name, self.__callback)

    def __callback(self, body):
        device_plant = None
        measurement = None

        try:
            measurement = MeasurementReadingSchema(**json.loads(body))
            logger.info(
                f"[ NEW PACKAGE RECEIVED FROM ID_DEVICE = {measurement.id_device} ]")
            logger.debug(f"[ PACKAGE: {body} ]")

            device_plant = obtain_device_plant(measurement, session)
            check_package(measurement)
            apply_rules(measurement, device_plant)
        except ValidationError as err:
            logger.info("[ INVALID PACKAGE RECEIVED ]")
            logger.debug(f"[ ERROR ] [ DETAIL: {err.errors()} ] [ PACKAGE: {body} ]")
        except RowNotFoundError as err:
            logger.info(f"[ DEVICE PLANT WITH ID = {err.primary_key} NOT FOUND ]")
            logger.debug(f"[ ERROR ] [ DETAIL: {err} ] [ PACKAGE: {body} ]")
            
            device_plant = None  # For not saving the measurement.
        except EmptyPackageError as err:
            logger.info("[ EMPTY PACKAGE RECEIVED ] [ READY TO SEND NOTIFICATION ]")
            logger.debug(f"[ ERROR ] [ DETAIL: {err} ] [ PACKAGE: {body} ]")

            send_notification(device_plant.id_user, err)

            measurement = None  # For not saving the measurement.
        except DeviatingParameters as err:
            logger.info("[ DEVIATING PARAMETERS ] [ READY TO SEND NOTIFICATION ]")
            logger.debug(f"[ ERROR ] [ DETAIL: {err} ] [ PACKAGE: {body} ]")

            # TO DO - Ticket HAN-17 & Step #4 from Ticket HAN-14
            parameters = err.parameters  # List of deviating parameters.
            send_notification(device_plant.id_user, err)

        if device_plant is not None and measurement is not None:
            try:
                save_measurement(measurement, device_plant, session)
            except InvalidInsertion as err:
                logger.error("[ INVALID INSERTION ]")
                logger.debug(f"[ ERROR ] [ DETAIL: {err} ] [ PACKAGE: {body} ]")
