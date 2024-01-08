from fastapi import FastAPI
from app.controller.calculator_controller import CalculatorController
from app.schemas.schemas import Request
from app.service.calculator_service import CalculatorService

app = FastAPI()
service = CalculatorService()
controller = CalculatorController(service)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/sum")
async def calculator(request: Request):
    return controller.handle_sum(request)
