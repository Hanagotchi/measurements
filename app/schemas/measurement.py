from pydantic import BaseModel, Field
from typing import Optional, Literal


class DeviatedParametersSchema(BaseModel):
    temperature: Optional[Literal['lower', "higher"]] = Field(default=None)
    humidity: Optional[Literal['lower', "higher"]] = Field(default=None)
    light: Optional[Literal['lower', "higher"]] = Field(default=None)
    watering: Optional[Literal['lower', "higher"]] = Field(default=None)

    def hasDeviations(self) -> bool:
        return (self.temperature is not None or
                self.humidity is not None or
                self.light is not None or
                self.watering is not None)


class Measurement(BaseModel):
    temperature: Optional[float]
    # Humedad del ambiente, nuestro sensor
    # de Xiaomi hhccjcy01 no lo mide
    humidity: Optional[int]
    light: Optional[float]
    # Nivel de riego, en nuestro sensor
    # se mide como moisture
    watering: Optional[int]


class MeasurementSavedSchema(Measurement):
    id: int
    id_plant: int
    plant_type: str
    time_stamp: str
    deviations: Optional[DeviatedParametersSchema] = Field(None)


class MeasurementReadingSchema(Measurement):
    """
        Schema used to parse the data from measurements obtained via RabbitMQ.
    """
    id_device: str
    time_stamp: str

    def is_partial(self) -> bool:
        return (self.temperature is None or
                self.light is None or
                self.watering is None)
