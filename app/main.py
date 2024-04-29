from fastapi import FastAPI
from database.database import SQLAlchemyClient
import logging
from controller.calculator_controller import CalculatorController
from schemas.schemas import Request as RequestSchema
from service.calculator_service import CalculatorService
from router import api_router


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
async def calculator(request: RequestSchema):
    return controller.handle_sum(request)

app.include_router(api_router)
