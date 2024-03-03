from sqlalchemy import create_engine, engine
from sqlalchemy.orm import Session
from database.models.number import Number
from os import environ


class CalculatorService:
    def __init__(self):
        engine_ = create_engine(engine.URL.create(
            "postgresql",
            database=environ["MEASUREMENTS_DB"],
            username=environ["POSTGRES_USER"],
            password=environ["POSTGRES_PASSWORD"],
            host=environ["POSTGRES_HOST"],
            port=environ["POSTGRES_PORT"]
        ), echo=True)
        self.session = Session(engine_)

    def add_number(self, number):
        self.session.add(Number(number=number))
        self.session.commit()
