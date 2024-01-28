from fastapi import APIRouter, Request, status
from schemas.measurement import (
    MeasurementSavedSchema
)
from controller import measurement_controller as controller


measurement = APIRouter()


@measurement.get(
        "/{id_plant}/last",
        status_code=status.HTTP_200_OK,
        response_model=MeasurementSavedSchema
        )
async def last_measurement_made_by_plant(id_plant: int, req: Request):
    return controller.last_measurement_made_by_plant(req, id_plant)
