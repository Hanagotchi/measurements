from pydantic import BaseModel, Field
from typing import Optional


class PlantSchema(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    scientific_name: str = Field(...)
    #plant_type_id: int = Field(...)
    id_user: int = Field(...)