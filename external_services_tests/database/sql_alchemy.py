from sqlalchemy import CheckConstraint, create_engine, Integer, String, SmallInteger, select, delete, update
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, Session
from database import Database
from dotenv import load_dotenv
from os import environ
from typing import Optional, Union

load_dotenv()

class Base(DeclarativeBase):
    pass

class DevicePlant(Base):
    __tablename__ = "device_plant"
    __table_args__ = {'schema': 'dev'}

    id_device: Mapped[str] = mapped_column(String(32), primary_key=True)
    id_plant: Mapped[int] = mapped_column(Integer, unique=True)
    plant_type: Mapped[int] = mapped_column(SmallInteger)
    id_user: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"DevicePlant(id_device={self.id_device}, id_plant={self.id_plant}, plant_type={self.plant_type}, id_user={self.id_user})"
    

class Measurement(Base):
    __tablename__ = "measurements"
    __table_args__ = {'schema': 'dev'}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_plant: Mapped[int] = mapped_column(Integer, unique=True)
    plant_type: Mapped[int] = mapped_column(SmallInteger)
    time_stamp: Mapped[str] = mapped_column(String(50))
    temperature: Mapped[Optional[int]] = mapped_column(SmallInteger)
    humidity: Mapped[Optional[int]] = mapped_column(SmallInteger)
    light: Mapped[Optional[int]] = mapped_column(SmallInteger)
    watering: Mapped[Optional[int]] = mapped_column(SmallInteger)

    __table_args__ = (
        CheckConstraint('humidity >= 0 AND humidity <= 100', name='check_humidity'),
        CheckConstraint('humidity >= 0 ', name='check_light'),
        CheckConstraint('humidity >= 0 AND humidity <= 100', name='check_watering'),
        {'schema': 'dev'}  
    )

    def __repr__(self):
        return f"Measurement(id={self.id!r}, id_plant={self.id_plant!r}, plant_type={self.plant_type!r}, time_stamp={self.time_stamp!r}, temperature={self.temperature!r}, humidity={self.humidity!r}, light={self.light!r}, watering={self.watering!r})"


class SQL_Alchemy():

    def __init__(self):
        db_url = f'postgresql://{environ["POSTGRES_USER"]}:{environ["POSTGRES_PASSWORD"]}@{environ["POSTGRES_HOST"]}:{environ["POSTGRES_PORT"]}/{environ["POSTGRES_DB"]}'
        self.engine = create_engine(db_url)
        self.conn = self.engine.connect()

        # If the schema wasn't created 
        # Base.metadata.create_all(self.engine)

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


    ### DEVICE_PLANT TABLE ###
    
    def find_device_plant(self, id_device: str) -> DevicePlant:

        query = select(DevicePlant).where(DevicePlant.id_device == id_device)

        with Session(self.engine) as session:
            result = session.scalars(query).one()
        
        return result
    
    def update_device_plant(self, id_device: str, id_plant: Optional[int], plant_type: Optional[int], id_user: Optional[int]):
        query = select(DevicePlant).where(DevicePlant.id_device == id_device)

        with Session(self.engine) as session:
            device_plant = session.scalars(query).one()
            if id_plant: device_plant.id_plant = id_plant
            if plant_type: device_plant.id_plant = plant_type
            if id_user: device_plant.id_user = id_user
            session.commit()

    ### MEASUREMENTS TABLE ###

    def get_last_measurement(self, id_plant: int) -> Measurement:
        query = select(Measurement).where(Measurement.id_plant == id_plant).order_by(Measurement.id.desc()).limit(1)

        with Session(self.engine) as session:
            result: Measurement = session.scalars(query).one()
        
        return result
