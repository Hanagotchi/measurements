from sqlalchemy import Integer, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from database.models.base import Base
from schemas.device_plant import DevicePlantSchema
from os import environ

SCHEMA = environ.get("POSTGRES_SCHEMA", "measurements")


class DevicePlant(Base):
    __tablename__ = "device_plant"
    __table_args__ = {'schema': SCHEMA}

    id_device: Mapped[str] = mapped_column(String(32), primary_key=True)
    id_plant: Mapped[int] = mapped_column(Integer, unique=True)
    plant_type: Mapped[int] = mapped_column(SmallInteger)
    id_user: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return (f"DevicePlant(id_device={self.id_device}, "
                f"id_plant={self.id_plant}, "
                f"plant_type={self.plant_type}, id_user={self.id_user})")

    @classmethod
    def from_pydantic(cls, pydantic_obj: DevicePlantSchema):
        return DevicePlant(
            id_device=pydantic_obj.id_device,
            id_plant=pydantic_obj.id_plant,
            plant_type=pydantic_obj.plant_type,
            id_user=pydantic_obj.id_user,
        )
