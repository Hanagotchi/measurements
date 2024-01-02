from sqlalchemy import CheckConstraint, create_engine, Integer, String, SmallInteger
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from database import Database
from dotenv import load_dotenv
from os import environ

Base = declarative_base()

class DevicePlant(Base):
    _tablename_ = "device_plant"
    _table_args_ = {'schema': 'dev'}

    id_device: Mapped[str] = mapped_column(String(32), primary_key=True)
    id_plant: Mapped[int] = mapped_column(Integer, unique=True)
    plant_type: Mapped[int] = mapped_column(SmallInteger)
    id_user: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"DevicePlant(id_device={self.id_device}, id_plant={self.id_plant}, plant_type={self.plant_type}, id_user={self.id_user})"
    
class Measurement(Base):
    _tablename_ = "measurements"
    _table_args_ = {'schema': 'dev'}

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
        CheckConstraint('humidity >= 0 ', name='check_humidity'),
        CheckConstraint('humidity >= 0 AND humidity <= 100', name='check_humidity'),
        {'schema': 'dev'}  
    )

    def __repr__(self):
        return f"Measurement(id={self.id!r}, id_plant={self.id_plant!r}, plant_type={self.plant_type!r}, timestamp={self.timestamp!r}, temperature={self.temperature!r}, humidity={self.humidity!r}, light={self.light!r}, watering={self.watering!r})"





class SQL_Alchemy(Database):

    def _init_(self):
        load_dotenv()


        db_url = f'postgresql://{environ["POSTGRES_USER"]}:{environ["POSTGRES_PASSWORD"]}@{environ["POSTGRES_HOST"]}:{environ["POSTGRES_PORT"]}/{environ["POSTGRES_DB"]}'
        self.engine = create_engine(db_url)
        self.conn= self.engine.connect()

    def shutdown(self):
        self.conn.close()

    def insert_into_device_plant(self, id_device, id_plant, plant_type, id_user):
        insert_query = "INSERT INTO dev.device_plant(id_device, id_plant, plant_type, id_user) VALUES (%s, %s, %s, %s)"
        self.conn.execute(insert_query, (id_device, id_plant, plant_type, id_user))
        self.conn.commit()