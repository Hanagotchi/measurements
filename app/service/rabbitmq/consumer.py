import os
import json
import logging
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


dbUrl = os.environ.get("DATABASE_URL")
engine = create_engine(dbUrl, echo=True, future=True)
session = Session(engine)


class Consumer:
    def __init__(self, queue_name):
        self.__queue_name = queue_name
        self.__middleware = Middleware()

    def run(self):
        self.__middleware.create_queue(self.__queue_name)
        self.__middleware.listen_on(self.__queue_name, self.__callback)

    def __callback(self, body):
        try:
            measurement = MeasurementReadingSchema(**json.loads(body))  
            logger.debug(f"[ NEW PACKAGE RECEIVED FROM ID_DEVICE = {measurement.id_device} ]")
            logger.debug(f"[ PACKAGE: {body} ]")
        except ValidationError as e:
            logger.warning("[ INVALID PACKAGE RECEIVED ]")
            logger.debug(f"[ ERROR DETAIL ] [ PACKAGE: {body} ] [ ERROR: {e.errors()} ]")