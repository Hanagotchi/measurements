import time
from service.common.middleware import Middleware
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os
import json

# TODO: agregar healthcheks en el docker compose
time.sleep(17)
middleware = Middleware()
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


def callback(body):
    print("Entro al callback")
    body = json.loads(body)
    print(body)
    dp = DevicePlant(id_device=body["id_device"],
                     id_plant=body["id_plant"],
                     plant_type=body["plant_type"],
                     id_user=body["id_user"])
    session.add(dp)
    session.commit()
    print("Se agrego a la base de datos")


def main():
    middleware.create_queue("device_plant")
    middleware.listen_on("device_plant", callback)


if __name__ == "__main__":
    main()
