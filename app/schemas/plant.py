from pydantic import BaseModel, Field


class PlantSchema(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    scientific_name: str = Field(...)
    id_user: int = Field(...)
