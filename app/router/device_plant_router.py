from fastapi import APIRouter, Body, Request, status
from schemas.device_plant import DevicePlantSchema, DevicePlantUpdateSchema
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


@device_plant.patch(
        "",
        status_code=status.HTTP_200_OK,
        response_model=DevicePlantSchema
        )
async def update_fields_in_device_plant(req: Request,
                                        device_plant_update_set:
                                        DevicePlantUpdateSchema = Body(...)):

    return controller.update_device_plant(req, device_plant_update_set)


@device_plant.put(
        "",
        status_code=status.HTTP_200_OK,
        response_model=DevicePlantSchema
        )
async def update_all_in_device_plant(req: Request,
                                     device_plant: DevicePlantSchema = Body(...)):

    return controller.update_device_plant(req, device_plant)
