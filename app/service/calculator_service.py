from sqlalchemy.orm import Session
from database.models.number import Number
from os import environ


class CalculatorService:
    def __init__(self):
        engine_ = environ.get("DATABASE_URL").replace("postgres://", "postgresql://", 1)
        self.session = Session(engine_)

    def add_number(self, number):
        self.session.add(Number(number=number))
        self.session.commit()
