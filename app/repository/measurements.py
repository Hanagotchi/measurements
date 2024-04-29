from os import environ
from typing import Optional, List, Union
from sqlalchemy import create_engine, select, delete, column
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from models.measurement import Measurement
from database.models.device_plant import DevicePlant
from .sql_exception_handling import withSQLExceptionsHandle


class MeasurementsRepository:
    db_url = environ.get("DATABASE_URL").replace("postgres://",
                                                 "postgresql://",
                                                 1)

    engine = create_engine(db_url)

    def __init__(self):
        self.conn = self.engine.connect()
        self.session = Session(self.engine)

    def shutdown(self):
        self.conn.close()
        self.session.close()

    def rollback(self):
        self.session.rollback()

    @withSQLExceptionsHandle()
    def add(self, record: Union[DevicePlant, Measurement]):
        self.session.add(record)
        self.session.commit()

    @withSQLExceptionsHandle()
    def create_device_plant_relation(self, plant, device_plant):
        device_plant = DevicePlant(
            id_device=device_plant.id_device,
            id_plant=device_plant.id_plant,
            plant_type=plant.scientific_name,
            id_user=plant.id_user,
        )
        self.session.add(device_plant)
        self.session.commit()

    @withSQLExceptionsHandle()
    def find_by_device_id(self, id_device: str) -> DevicePlant:
        query = select(DevicePlant).where(DevicePlant.id_device == id_device)
        result = self.session.scalars(query).one()
        return result

    @withSQLExceptionsHandle()
    def find_by_plant_id(self, id_plant: str) -> Optional[dict]:
        try:
            query = select(DevicePlant).where(DevicePlant.id_plant == id_plant)
            result = self.session.scalars(query).one()
            return self.__device_plant_to_dict(result)
        except NoResultFound:
            return None

    @withSQLExceptionsHandle()
    def find_all(self, limit: int) -> Optional[List[DevicePlant]]:
        try:
            query = select(DevicePlant).limit(limit)
            results = self.session.scalars(query).all()
            return [self.__device_plant_to_dict(result) for result in results]
        except NoResultFound:
            return None

    @withSQLExceptionsHandle()
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

    @withSQLExceptionsHandle()
    def get_plant_last_measurement(self, id_plant: int) -> Measurement:
        try:
            query = select(Measurement).where(
                Measurement.id_plant == id_plant
            ).order_by(Measurement.id.desc()).limit(1)
            result = self.session.scalars(query).one()
            return result
        except NoResultFound:
            return None

    @withSQLExceptionsHandle()
    def delete_by_field(self, field: str, value: str) -> int:
        query = delete(DevicePlant).where(column(field) == value)
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount

    def __device_plant_to_dict(self, device_plant: DevicePlant) -> dict:
        return {
            "id_device": device_plant.id_device,
            "id_plant": device_plant.id_plant,
            "plant_type": device_plant.plant_type,
            "id_user": device_plant.id_user
        }
