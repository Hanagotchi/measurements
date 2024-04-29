from sqlalchemy import create_engine, select, delete, column
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from os import environ
from typing import Optional, Sequence, Union

from database.models.device_plant import DevicePlant
from database.models.measurement import Measurement

load_dotenv()


class SQLAlchemyClient():
    db_url = environ.get("DATABASE_URL").replace("postgres://", "postgresql://", 1)

    engine = create_engine(db_url)

    def __init__(self):
        self.conn = self.engine.connect()
        self.session = Session(self.engine)

    def shutdown(self):
        self.conn.close()
        self.session.close()

    def rollback(self):
        self.session.rollback()

    def clean_table(self, table: Union[DevicePlant, Measurement]):
        query = delete(table)  # type: ignore
        self.session.execute(query)
        self.session.commit()

    def add(self, record: Union[DevicePlant, Measurement]):
        self.session.add(record)
        self.session.commit()

    def find_by_device_id(self, id_device: str) -> DevicePlant:
        query = select(DevicePlant).where(DevicePlant.id_device == id_device)
        result = self.session.scalars(query).one()
        return result

    def find_by_plant_id(self, id_plant: str) -> DevicePlant:
        query = select(DevicePlant).where(DevicePlant.id_plant == id_plant)
        result = self.session.scalars(query).one()
        return result

    def find_all(self, limit: int) -> Sequence[DevicePlant]:
        query = select(DevicePlant).limit(limit)
        result = self.session.scalars(query).all()
        return result

    def update_device_plant(self,
                            id_device: str,
                            id_plant: Optional[int],
                            plant_type: Optional[str],
                            id_user: Optional[int]):

        query = select(DevicePlant).where(DevicePlant.id_device == id_device)

        device_plant = self.session.scalars(query).one()
        if id_plant:
            device_plant.id_plant = id_plant
        if plant_type:
            device_plant.plant_type = plant_type
        if id_user:
            device_plant.id_user = id_user
        self.session.commit()

    def get_last_measurement(self, id_plant: int) -> Measurement:
        query = select(Measurement).where(
            Measurement.id_plant == id_plant
        ).order_by(Measurement.id.desc()).limit(1)
        result: Measurement = self.session.scalars(query).one()
        return result

    def delete_by_field(self, field: str, value: str) -> int:
        query = delete(DevicePlant).where(column(field) == value)
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount
