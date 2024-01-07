from fastapi import Body, FastAPI, Request
from app.database.database import SQLAlchemyClient
from app.database.models.DevicePlant import DevicePlant

app = FastAPI()

@app.on_event("startup")
async def start_up():
    app.database = SQLAlchemyClient()


@app.on_event("shutdown")
async def shutdown_db_client():
    app.database.shutdown()
    


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/device-plant")
async def add_new_device_plant(req: Request, device_plant: DevicePlant = Body(...)):
    req.app.database.add_new(device_plant)
    return req.app.database.find_device_plant(device_plant.id_device)

