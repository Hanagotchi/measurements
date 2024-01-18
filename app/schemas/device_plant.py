from pydantic import BaseModel, Field


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
