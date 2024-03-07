from pydantic import BaseModel, Field

class PlantTypeSchema(BaseModel):
    botanical_name: str = Field(..., max_length=70)
    id: int = Field(..., gt=0)
    common_name: str = Field(..., max_length=70)
    description: str = Field(..., max_length=1000)
    cares: str = Field(..., max_length=1000)
    photo_link: str = Field(..., max_length=160)