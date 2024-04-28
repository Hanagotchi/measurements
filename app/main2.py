import logging
from fastapi import FastAPI

from controller.measurements import MeasurementsController
from service.measurements import MeasurementsService
from repository.measurements import MeasurementsRepository
from schemas.measurement import MeasurementSavedSchema


app = FastAPI()
repository = MeasurementsRepository()
service = MeasurementsService(repository)
controller = MeasurementsController(service)

logger = logging.getLogger("measurements")
logger.setLevel("DEBUG")


# @app.on_event("startup")
# async def start_up():
#     app.logger = logger

#     try:
#         app.database = SQLAlchemyClient()
#         app.logger.info("Postgres connection established")
#     except Exception as e:
#         app.logger.error(e)
#         app.logger.error("Could not connect to Postgres client")


# @app.on_event("shutdown")
# async def shutdown_db_client():
#     app.database.shutdown()
#     app.logger.info("Postgres shutdown succesfully")


@app.get("/")
async def root():
    return {"message": "measurments service"}


@app.get("/measurements/{id_plant}/last", response_model=MeasurementSavedSchema)
async def get_plant_measurements(id_plant: int):
    return controller.handle_get_plant_last_measurement(id_plant)


# @app.post("/device-plant", response_model=DevicePlantSchema)
# async def create_device_plant_relation(req: Request,
#                                        device_plant: DevicePlantCreateSchema):
#     return await controller.create_device_plant_relation(req, device_plant)


# @app.patch("/device-plant/{id_device}", response_model=DevicePlantSchema)
# async def update_fields_in_device_plant(
#     id_device: str,
#     req: Request,
#     device_plant_update_set:
#     DevicePlantPartialUpdateSchema = Body(...)
# ):
#     return await controller.update_device_plant(
#         req, id_device, device_plant_update_set
#     )


# @app.put("/device-plant/{id_device}", response_model=DevicePlantSchema)
# async def update_all_in_device_plant(
#     id_device: str,
#     req: Request,
#     device_plant: DevicePlantUpdateSchema = Body(...)
# ):
#     return await controller.update_device_plant(req, id_device, device_plant)


# @app.get("/device-plant", response_model=List[DevicePlantSchema])
# async def get_device_plant(
#     req: Request,
#     id_plant: int = Query(None),
#     limit: int = Query(10)
# ):
#     if id_plant is None:
#         return controller.get_all_device_plant_relations(req, limit)
#     return [controller.get_device_plant_relation(req, id_plant)]


# @app.delete("/device-plant/{id}")
# async def delete_device_plant_relation(
#     response: Response, req: Request,
#     type_id: Literal["id_device", "id_plant"],
#     id: str
# ):
#     return controller.delete_device_plant_relation(req, response, type_id, id)