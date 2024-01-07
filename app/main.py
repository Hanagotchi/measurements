from fastapi import Body, FastAPI, Request
from app.database.database import SQLAlchemyClient
from app.database.models.DevicePlant import DevicePlant
from app.schemas.DevicePlant import DevicePlantSchema
import logging

app = FastAPI()
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


# Endpoint only for DB conection testing.
@app.post("/device-plant")
async def add_new_device_plant(req: Request, device_plant: DevicePlantSchema = Body(...)):
    req.app.database.add_new(DevicePlant.from_pydantic(device_plant))
    return req.app.database.find_device_plant(device_plant.id_device)

