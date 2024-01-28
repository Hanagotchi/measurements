from pydantic import BaseModel
from typing import Optional


class MeasurementSavedSchema(BaseModel):
    id: int
    id_plant: int
    plant_type: int
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
