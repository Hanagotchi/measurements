import logging
from typing import List, Literal
from fastapi import FastAPI, Depends, Header

from controller.measurements import MeasurementsController
from service.measurements import MeasurementsService
from external.Plants import PlantsService
from repository.measurements import MeasurementsRepository
from schemas.measurement import MeasurementSavedSchema
from schemas.device_plant import (
    DevicePlantSchema,
    DevicePlantCreateSchema,
    DevicePlantPartialUpdateSchema
)
from query_params.QueryParams import DevicePlantQueryParams


app = FastAPI()
repository = MeasurementsRepository()
service = MeasurementsService(repository)
plants_service = PlantsService()
controller = MeasurementsController(service, plants_service)

logger = logging.getLogger("measurements")
logger.setLevel("DEBUG")


# I'll leave this as a getter, in case its implementation changes
async def get_access_token(x_access_token: str = Header(...)):
    return x_access_token


@app.get("/")
async def root():
    return {"message": "measurments service"}


@app.get("/measurements/{id_plant}/last", response_model=MeasurementSavedSchema)
async def get_plant_measurements(id_plant: int, token: str = Depends(get_access_token)):
    return await controller.handle_get_plant_last_measurement(id_plant, token)


@app.post("/measurements/device-plant", response_model=DevicePlantSchema)
async def create_device_plant_relation(device_plant: DevicePlantCreateSchema,
                                       token: str = Depends(get_access_token)):
    return await controller.handle_create_device_plant_relation(device_plant.dict(),
                                                                token)


@app.patch("/measurements/device-plant/{id_device}", response_model=DevicePlantSchema)
async def update_fields_in_device_plant(id_device: str,
                                        update_device_plant_info:
                                        DevicePlantPartialUpdateSchema,
                                        token: str = Depends(get_access_token)):
    return await controller.handle_update_device_plant(id_device,
                                                       update_device_plant_info.dict(),
                                                       token)


@app.get("/measurements/device-plant", response_model=List[DevicePlantSchema])
async def get_device_plant(
    query_params: DevicePlantQueryParams = Depends(DevicePlantQueryParams),
    token: str = Depends(get_access_token)
):
    return await controller.handle_get_device_plant(query_params.get_query_params(),
                                                    token)


@app.delete("/measurements/device-plant/{id}")
async def delete_device_plant_relation(
    type_id: Literal["id_device", "id_plant"],
    id: str,
    token: str = Depends(get_access_token)
):
    return await controller.handle_delete_device_plant_relation(type_id, id, token)
