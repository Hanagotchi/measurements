from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    device_token: str = Field(...)
