import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models.number import Number


class CalculatorService:
    def __init__(self):
        engine = create_engine(os.environ.get('DATABASE_URL'), echo=True)
        self.session = Session(engine)

    def add_number(self, number):
        self.session.add(Number(number=number))
        self.session.commit()
