from fastapi import Request
from database.models.device_plant import DevicePlant
from schemas.device_plant import DevicePlantSchema


def create_device_plant_relation(req: Request, device_plant: DevicePlantSchema):
    try:
        req.app.database.add_new(DevicePlant.from_pydantic(device_plant))
        return req.app.database.find_device_plant(device_plant.id_device)
    except Exception as e:
        req.app.database.rollback()
        raise e
