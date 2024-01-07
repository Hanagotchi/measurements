from sqlalchemy import CheckConstraint, Integer, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from app.database.models.Base import Base


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
        return f"Measurement(id={self.id!r}, id_plant={self.id_plant!r}, plant_type={self.plant_type!r}, time_stamp={self.time_stamp!r}, temperature={self.temperature!r}, humidity={self.humidity!r}, light={self.light!r}, watering={self.watering!r})"
