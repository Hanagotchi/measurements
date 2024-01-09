import os
import json
import logging
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from ..common.middleware import Middleware

Base = declarative_base(metadata=MetaData(schema='dev'))


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
        body = json.loads(body)
        print(body)
        dp = DevicePlant(id_device=body["id_device"],
                         id_plant=body["id_plant"],
                         plant_type=body["plant_type"],
                         id_user=body["id_user"])
        session.add(dp)
        session.commit()
        logging.info('action: resgitro agregado a la base de datos|'
                     f"device_plant: {dp}")
