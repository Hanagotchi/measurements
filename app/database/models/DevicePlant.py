from sqlalchemy import Integer, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.database.models.Base import Base
from app.schemas.DevicePlant import DevicePlantSchema


class DevicePlant(Base):
    __tablename__ = "device_plant"
    __table_args__ = {'schema': 'dev'}

    id_device: Mapped[str] = mapped_column(String(32), primary_key=True)
    id_plant: Mapped[int] = mapped_column(Integer, unique=True)
    plant_type: Mapped[int] = mapped_column(SmallInteger)
    id_user: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return format(
            "DevicePlant(id_device={0}, id_plant={1}, plant_type={2}, id_user={3})",
            self.id_device,
            self.id_plant,
            self.plant_type,
            self.id_user,
        )

    @classmethod
    def from_pydantic(cls, pydantic_obj: DevicePlantSchema):
        return DevicePlant(
            id_device=pydantic_obj.id_device,
            id_plant=pydantic_obj.id_plant,
            plant_type=pydantic_obj.plant_type,
            id_user=pydantic_obj.id_user,
        )
