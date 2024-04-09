from sqlalchemy import CheckConstraint, Integer, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from database.models.base import Base
from os import environ


SCHEMA = environ.get("POSTGRES_SCHEMA", "measurements_service")


class Measurement(Base):
    __tablename__ = "measurements"
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_plant: Mapped[int] = mapped_column(Integer)
    plant_type: Mapped[str] = mapped_column(String(70))
    time_stamp: Mapped[str] = mapped_column(String(50))
    temperature: Mapped[Optional[int]] = mapped_column(SmallInteger)
    humidity: Mapped[Optional[int]] = mapped_column(SmallInteger)
    light: Mapped[Optional[int]] = mapped_column(SmallInteger)
    watering: Mapped[Optional[int]] = mapped_column(SmallInteger)

    __table_args__ = (
        CheckConstraint(
            'humidity >= 0 AND humidity <= 100',
            name='check_humidity'
        ),
        CheckConstraint('humidity >= 0 ', name='check_light'),
        CheckConstraint(
            'humidity >= 0 AND humidity <= 100',
            name='check_watering'
        ),
        {'schema': SCHEMA}
    )

    def __repr__(self):
        return (f"Measurement(id={self.id}, "
                f"id_plant={self.id_plant}, "
                f"plant_type={self.plant_type}, "
                f"time_stamp={self.time_stamp}, "
                f"temperature={self.temperature}, "
                f"humidity={self.humidity}, "
                f"light={self.light}, "
                f"watering={self.watering})")
