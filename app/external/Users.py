import logging
from httpx import (
    AsyncClient,
    codes,
    HTTPStatusError
)
from os import environ
from fastapi import HTTPException
from typing import Optional
from schemas.user import UserSchema

logger = logging.getLogger("app")
logger.setLevel("DEBUG")

USERS_SERVICE_URL = environ["USERS_SERVICE_URL"]


class UsersService():
    @staticmethod
    async def get_user(user_id: int) -> Optional[UserSchema]:
        try:
            async with AsyncClient() as client:
                response = await client.get(
                    USERS_SERVICE_URL + f"/users/{user_id}"
                )
                if response.status_code == codes.OK:
                    message = response.json()["message"]
                    return UserSchema(id=message["id"], name=message["name"],
                                      device_token=message["device_token"])
                elif response.status_code == codes.NOT_FOUND:
                    return None
                else:
                    return response.raise_for_status().json()

        except HTTPStatusError as e:
            logger.error(
                "Users service cannot be accessed because: " + str(e)
                )
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.content.decode(),
            )

    @staticmethod
    async def get_user_id(token: str) -> int:
        try:
            async with AsyncClient() as client:
                response = await client.post(
                    USERS_SERVICE_URL + "/users/token", json={"token": token}
                )
                response.raise_for_status()
                user_id = response.json().get("user_id")
                return user_id

        except HTTPStatusError as e:
            logger.error("Error while getting user ID: " + str(e))
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.content.decode(),
            )
