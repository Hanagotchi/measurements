from sqlalchemy import CheckConstraint, create_engine, Integer, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from database import Database
from dotenv import load_dotenv
from os import environ

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
    timestamp: Mapped[str] = mapped_column(String(50))
    temperature: Mapped[int] = mapped_column(SmallInteger)
    humidity: Mapped[int] = mapped_column(SmallInteger)
    light: Mapped[int] = mapped_column(SmallInteger)
    watering: Mapped[int] = mapped_column(SmallInteger)

    __table_args__ = (
        CheckConstraint('humidity >= 0 AND humidity <= 100', name='check_humidity'),
        CheckConstraint('humidity >= 0 ', name='check_light'),
        CheckConstraint('humidity >= 0 AND humidity <= 100', name='check_watering'),
        {'schema': 'dev'}  
    )

    def __repr__(self):
        return f"Measurement(id={self.id!r}, id_plant={self.id_plant!r}, plant_type={self.plant_type!r}, timestamp={self.timestamp!r}, temperature={self.temperature!r}, humidity={self.humidity!r}, light={self.light!r}, watering={self.watering!r})"


class SQL_Alchemy:

    def __init__(self):

        db_url = f'postgresql://{environ["POSTGRES_USER"]}:{environ["POSTGRES_PASSWORD"]}@{environ["POSTGRES_HOST"]}:{environ["POSTGRES_PORT"]}/{environ["POSTGRES_DB"]}'
        self.engine = create_engine(db_url)
        self.conn = self.engine.connect()
        Base.metadata.create_all(self.engine)

    def shutdown(self):
        self.conn.close()