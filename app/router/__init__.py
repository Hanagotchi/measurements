from fastapi import APIRouter
from router.device_plant_router import device_plant
from router.measurement_router import measurement

api_router = APIRouter()

api_router.include_router(device_plant, tags=["DevicePlant"], prefix="/device-plant")
api_router.include_router(measurement, tags=["Measurement"], prefix="/measurement")
