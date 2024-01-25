from fastapi import APIRouter, Body, Request, status
from schemas.measurement import (
    MeasurementSavedSchema
)
from fastapi import Request, status, HTTPException

measurement = APIRouter()

@measurement.get(
        "/{id_plant}/last",
        status_code=status.HTTP_200_OK,
        response_model=MeasurementSavedSchema
        )
async def last_measurement_made_by_device(req: Request, id_plant: int):
    raise HTTPException(status_code=501, detail="Not implemented :c")