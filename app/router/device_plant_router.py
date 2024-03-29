from typing import List, Literal

from fastapi import APIRouter, Body, Response, Request, status, Query
from schemas.device_plant import (
    DevicePlantCreateSchema,
    DevicePlantPartialUpdateSchema,
    DevicePlantSchema,
    DevicePlantUpdateSchema
)
from controller import device_plant_controller as controller

device_plant = APIRouter()


@device_plant.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=DevicePlantSchema
)
async def create_device_plant_relation(
    req: Request,
    device_plant: DevicePlantCreateSchema = Body(...)
):
    return await controller.create_device_plant_relation(req, device_plant)


@device_plant.patch(
    "/{id_device}",
    status_code=status.HTTP_200_OK,
    response_model=DevicePlantSchema
)
async def update_fields_in_device_plant(
    id_device: str,
    req: Request,
    device_plant_update_set:
    DevicePlantPartialUpdateSchema = Body(...)
):
    return await controller.update_device_plant(
        req, id_device, device_plant_update_set
    )


@device_plant.put(
    "/{id_device}",
    status_code=status.HTTP_200_OK,
    response_model=DevicePlantSchema
)
async def update_all_in_device_plant(
    id_device: str,
    req: Request,
    device_plant: DevicePlantUpdateSchema = Body(...)
):
    return await controller.update_device_plant(req, id_device, device_plant)


@device_plant.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[DevicePlantSchema]
)
async def get_device_plant(
    req: Request,
    id_plant: int = Query(None),
    limit: int = Query(10)
):
    if id_plant is None:
        return controller.get_all_device_plant_relations(req, limit)
    return [controller.get_device_plant_relation(req, id_plant)]


@device_plant.delete(
    "/{id}",
    status_code=status.HTTP_200_OK
)
async def delete_device_plant_relation(
    response: Response, req: Request,
    type_id: Literal["id_device", "id_plant"],
    id: str
):
    return controller.delete_device_plant_relation(req, response, type_id, id)
