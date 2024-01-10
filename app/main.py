from fastapi import FastAPI, Request, Body
from app.database.database import SQLAlchemyClient
from app.database.models.DevicePlant import DevicePlant
from app.schemas.DevicePlant import DevicePlantSchema
import logging
from app.controller.calculator_controller import CalculatorController
from app.schemas.schemas import Request
from app.service.calculator_service import CalculatorService

app = FastAPI()
service = CalculatorService()
controller = CalculatorController(service)

logger = logging.getLogger("measurements")
logger.setLevel("DEBUG")


@app.on_event("startup")
async def start_up():
    app.logger = logger

    try:
        app.database = SQLAlchemyClient()
        app.logger.info("Postgres connection established")
    except Exception as e:
        app.logger.error(e)
        app.logger.error("Could not connect to Postgres client")


@app.on_event("shutdown")
async def shutdown_db_client():
    app.database.shutdown()
    app.logger.info("Postgres shutdown succesfully")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/sum")
async def calculator(request: Request):
    return controller.handle_sum(request)


# Endpoint only for DB conection testing.
@app.post("/device-plant")
async def add_new_device_plant(req: Request,
                               device_plant: DevicePlantSchema = Body(...)):
    try:
        req.app.database.add_new(DevicePlant.from_pydantic(device_plant))
        return req.app.database.find_device_plant(device_plant.id_device)
    except Exception as e:
        req.app.database.rollback()
        raise e
