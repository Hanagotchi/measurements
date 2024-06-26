import logging
from httpx import (
    AsyncClient,
    AsyncHTTPTransport,
    codes,
    HTTPStatusError
)
from os import environ
from fastapi import HTTPException
from schemas.plant import PlantSchema
from typing import Optional

from schemas.plant_type import PlantTypeSchema


logger = logging.getLogger("app")
logger.setLevel("DEBUG")

PLANT_SERVICE_URL = environ["PLANT_SERVICE_URL"]
NUMBER_OF_RETRIES = 3
TIMEOUT = 10


class PlantsService():
    @staticmethod
    async def get_plant(plant_id: int) -> Optional[PlantSchema]:
        try:
            async with AsyncClient(
                transport=AsyncHTTPTransport(retries=NUMBER_OF_RETRIES),
                timeout=TIMEOUT
            ) as client:
                response = await client.get(
                    PLANT_SERVICE_URL + f"/plants/{plant_id}"
                )
                if response.status_code == codes.OK:
                    return PlantSchema(**response.json())
                elif response.status_code == codes.NOT_FOUND:
                    return None
                else:
                    return response.raise_for_status().json()

        except HTTPStatusError as e:
            logger.error(
                "Plant service cannot be accessed because: " + str(e)
                )
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.content.decode(),
            )

    @staticmethod
    async def get_plant_type(botanical_name: str) -> Optional[PlantTypeSchema]:
        try:
            async with AsyncClient(
                transport=AsyncHTTPTransport(retries=NUMBER_OF_RETRIES),
                timeout=TIMEOUT
            ) as client:
                response = await client.get(
                    PLANT_SERVICE_URL + f"/plant-type/{botanical_name}"
                )
                if response.status_code == codes.OK:
                    return PlantTypeSchema(**response.json())
                elif response.status_code == codes.NOT_FOUND:
                    return None
                else:
                    return response.raise_for_status().json()

        except HTTPStatusError as e:
            logger.error(
                "Plant service cannot be accessed because: " + str(e)
                )
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.content.decode(),
            )
