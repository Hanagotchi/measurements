from sqlalchemy import Column, Integer
from database.models.base import Base
from os import environ


class Number(Base):
    __tablename__ = 'numbers'
    __table_args__ = {'schema': environ.get("POSTGRES_SCHEMA", "measurements_service")}
    number = Column(Integer, primary_key=True)
