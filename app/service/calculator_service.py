from sqlalchemy import create_engine, engine
from sqlalchemy.orm import Session
from database.models.number import Number
from os import environ


class CalculatorService:
    def __init__(self):
        engine_ = create_engine(environ.get("HEROKU_DATABASE_URL", engine.URL.create(
            "postgres",
            database=environ.get("MEASUREMENTS_DB", "measurements"),
            username=environ.get("POSTGRES_USER", "user"),
            password=environ.get("POSTGRES_PASSWORD", "1234"),
            host=environ.get("POSTGRES_HOST", "sql"),
            port=environ.get("POSTGRES_PORT", "5432")
        )).replace("postgres://", "postgresql://", 1), echo=True)
        self.session = Session(engine_)

    def add_number(self, number):
        self.session.add(Number(number=number))
        self.session.commit()
