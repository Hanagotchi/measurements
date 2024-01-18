from fastapi import APIRouter, Body, Request, status
from schemas.device_plant import DevicePlantSchema
from controller import device_plant_controller as controller

device_plant = APIRouter()


@device_plant.post(
        "",
        status_code=status.HTTP_201_CREATED,
        response_model=DevicePlantSchema
        )
async def create_device_plant_relation(req: Request,
                                       device_plant: DevicePlantSchema = Body(...)):
    return controller.create_device_plant_relation(req, device_plant)
