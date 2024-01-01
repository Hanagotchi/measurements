from sqlalchemy import create_engine, Column, Integer, String
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