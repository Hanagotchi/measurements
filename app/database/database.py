from sqlalchemy import create_engine, select, delete, engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from os import environ
from typing import Optional, Union

from app.database.models.DevicePlant import DevicePlant
from app.database.models.Measurement import Measurement

load_dotenv()


class SQLAlchemyClient():

    db_url = engine.URL.create(
        "postgresql",
        database=environ["POSTGRES_DB"],
        username=environ["POSTGRES_USER"],
        password=environ["POSTGRES_PASSWORD"],
        host=environ["POSTGRES_HOST"],
        port=environ["POSTGRES_PORT"]
    )

    engine = create_engine(db_url)

    def __init__(self):
        self.conn = self.engine.connect()

    def shutdown(self):
        self.conn.close()

    def clean_table(self, table: Union[DevicePlant, Measurement]):
        with Session(self.engine) as session:
            query = delete(table)
            session.execute(query)
            session.commit()

    def add_new(self, record: Union[DevicePlant, Measurement]):
        with Session(self.engine) as session:
            session.add(record)
            session.commit()

    def find_device_plant(self, id_device: str) -> DevicePlant:

        query = select(DevicePlant).where(DevicePlant.id_device == id_device)

        with Session(self.engine) as session:
            result = session.scalars(query).one()

        return result

    def update_device_plant(self,
                            id_device: str,
                            id_plant: Optional[int],
                            plant_type: Optional[int],
                            id_user: Optional[int]):

        query = select(DevicePlant).where(DevicePlant.id_device == id_device)

        with Session(self.engine) as session:
            device_plant = session.scalars(query).one()
            if id_plant:
                device_plant.id_plant = id_plant
            if plant_type:
                device_plant.id_plant = plant_type
            if id_user:
                device_plant.id_user = id_user
            session.commit()

    def get_last_measurement(self, id_plant: int) -> Measurement:
        query = select(Measurement).where(
            Measurement.id_plant == id_plant
        ).order_by(Measurement.id.desc()).limit(1)

        with Session(self.engine) as session:
            result: Measurement = session.scalars(query).one()

        return result
