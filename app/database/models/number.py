from sqlalchemy import Column, Integer
from database.models.base import Base


class Number(Base):
    __tablename__ = 'numbers'
    number = Column(Integer, primary_key=True)
