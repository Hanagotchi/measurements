from sqlalchemy import Column, Integer

from app.models.database import Base


class Number(Base):
    __tablename__ = 'numbers'
    number = Column(Integer, primary_key=True)
