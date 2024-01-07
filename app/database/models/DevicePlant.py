from sqlalchemy import Integer, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.database.models.Base import Base


class DevicePlant(Base):
    __tablename__ = "device_plant"
    __table_args__ = {'schema': 'dev'}

    id_device: Mapped[str] = mapped_column(String(32), primary_key=True)
    id_plant: Mapped[int] = mapped_column(Integer, unique=True)
    plant_type: Mapped[int] = mapped_column(SmallInteger)
    id_user: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"DevicePlant(id_device={self.id_device}, id_plant={self.id_plant}, plant_type={self.plant_type}, id_user={self.id_user})"