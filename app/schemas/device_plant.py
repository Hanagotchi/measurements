from pydantic import BaseModel, Field
from typing import Optional


class DevicePlantSchema(BaseModel):
    id_device: str = Field(...)
    id_plant: int = Field(...)
    plant_type: int = Field(...)
    id_user: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id_device": "1",
                "id_plant": 1,
                "plant_type": 1,
                "id_user": 1
            }
        }


class DevicePlantUpdateSchema(BaseModel):
    id_device: str
    id_plant: Optional[int] = None
    plant_type: Optional[int] = None
    id_user: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "id_device": "1",
                "id_plant": 1,
                "plant_type": 1,
            }
        }
