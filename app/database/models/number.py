from sqlalchemy import Column, Integer
from database.models.base import Base
from os import environ


class Number(Base):
    __tablename__ = 'numbers'
    __table_args__ = {'schema': environ.get("MEASUREMENTS_SCHEMA", "dev")}
    number = Column(Integer, primary_key=True)
