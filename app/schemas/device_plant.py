from pydantic import BaseModel, Field
from typing import Optional


class DevicePlantCreateSchema(BaseModel):
    id_device: str = Field(...)
    id_plant: int = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "id_device": "1",
                "id_plant": 1,
            }
        }


class DevicePlantSchema(DevicePlantCreateSchema):
    plant_type: str = Field(..., max_length=70)
    id_user: int = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "id_device": "1",
                "id_plant": 1,
                "plant_type": "Duranta erecta",
                "id_user": 1
            }
        }


class DevicePlantUpdateSchema(BaseModel):
    id_plant: int = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "id_plant": 1,
            }
        }


class DevicePlantPartialUpdateSchema(BaseModel):
    id_plant: Optional[int] = Field(default=None, gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "id_plant": 1,
            }
        }
