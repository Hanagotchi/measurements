from pydantic import BaseModel


class DevicePlantSchema(BaseModel):
    id_device: str
    id_plant: int
    plant_type: int
    id_user: int
