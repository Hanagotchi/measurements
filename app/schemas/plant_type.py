from pydantic import BaseModel, Field

class PlantTypeSchema(BaseModel):
    botanical_name: str = Field(..., max_length=70)
    id: int = Field(..., gt=0)
    common_name: str = Field(..., max_length=70)
    description: str = Field(..., max_length=600)
    cares: str = Field(..., max_length=600)
    photo_link: str = Field(..., max_length=120)