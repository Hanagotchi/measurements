from pydantic import BaseModel, Field
from typing import Optional


class DevicePlantSchema(BaseModel):
    id_device: str = Field(...)
    id_plant: int = Field(..., gt=0)
    plant_type: int = Field(..., gt=0)
    id_user: int = Field(..., gt=0)

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
    id_plant: int = Field(..., gt=0)
    plant_type: int = Field(..., gt=0)
    id_user: int = Field(..., gt=0)

    class Config:
        schema_extra = {
            "example": {
                "id_plant": 1,
                "plant_type": 1,
                "id_user": 1,
            }
        }


class DevicePlantPartialUpdateSchema(BaseModel):
    id_plant: Optional[int] = Field(default=None, gt=0)
    plant_type: Optional[int] = Field(default=None, gt=0)
    id_user: Optional[int] = Field(default=None, gt=0)

    class Config:
        schema_extra = {
            "example": {
                "id_plant": 1,
                "plant_type": 1,
            }
        }
