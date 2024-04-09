from pydantic import BaseModel, Field
from typing import Optional, Literal

class DeviatedParameters(BaseModel):
    temperature: Optional[Literal['lower', "higher"]] = Field(default=None)
    humidity: Optional[Literal['lower', "higher"]] = Field(default=None)
    light: Optional[Literal['lower', "higher"]] = Field(default=None)
    watering: Optional[Literal['lower', "higher"]] = Field(default=None)

    def hasDeviations(self) -> bool:
        return (self.temperature is not None or 
                self.humidity is not None or 
                self.light is not None or 
                self.watering is not None)

class MeasurementSavedSchema(BaseModel):
    id: int
    id_plant: int
    plant_type: str
    time_stamp: str
    temperature: Optional[int]
    humidity: Optional[int]
    light: Optional[int]
    watering: Optional[int]


class MeasurementReadingSchema(BaseModel):
    """
        Schema used to parse the data from measurements obtained via RabbitMQ.
    """
    temperature: Optional[int]
    humidity: Optional[int]
    light: Optional[int]
    watering: Optional[int]
    id_device: str
    time_stamp: str
