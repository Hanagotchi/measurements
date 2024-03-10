from pydantic import BaseModel


class Request(BaseModel):
    number1: int
    number2: int
