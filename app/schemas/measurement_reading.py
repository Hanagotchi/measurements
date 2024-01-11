from pydantic import BaseModel
from typing import Optional

class MeasurementReadingSchema(BaseModel):
    """
        Schema used to parse the data from measurements obtained via RabbitMQ.
    """
    temperature: Optional[int]
    humidity: Optional[int]
    light: Optional[int]
    watering: Optional[int]
    id_device: int
    time_stamp: str