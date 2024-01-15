from sqlalchemy import CheckConstraint, Integer, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from database.models.base import Base


class Measurement(Base):
    __tablename__ = "measurements"
    __table_args__ = {'schema': 'dev'}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_plant: Mapped[int] = mapped_column(Integer, unique=True)
    plant_type: Mapped[int] = mapped_column(SmallInteger)
    time_stamp: Mapped[str] = mapped_column(String(50))
    temperature: Mapped[Optional[int]] = mapped_column(SmallInteger)
    humidity: Mapped[Optional[int]] = mapped_column(SmallInteger)
    light: Mapped[Optional[int]] = mapped_column(SmallInteger)
    watering: Mapped[Optional[int]] = mapped_column(SmallInteger)

    __table_args__ = (
        CheckConstraint('humidity >= 0 AND humidity <= 100', name='check_humidity'),
        CheckConstraint('humidity >= 0 ', name='check_light'),
        CheckConstraint('humidity >= 0 AND humidity <= 100', name='check_watering'),
        {'schema': 'dev'}
    )

    def __repr__(self):
        return format(
            ("Measurement(id={0!r}, id_plant={1!r}, "
             "plant_type={2!r}, time_stamp={3!r}, "
             "temperature={4!r}, humidity={5!r}, "
             "light={6!r}, watering={7!r})"),
            self.id,
            self.id_plant,
            self.plant_type,
            self.time_stamp,
            self.temperature,
            self.humidity,
            self.light,
            self.watering
        )
