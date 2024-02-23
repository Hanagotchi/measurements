import logging
from httpx import (
    AsyncClient,
    codes
)
from os import environ
from fastapi import status, HTTPException
from schemas.plant import PlantSchema
from typing import Optional


logger = logging.getLogger("app")
logger.setLevel("DEBUG")

PLANT_SERVICE_URL = environ["PLANT_SERVICE_URL"]


class PlantService():
    @staticmethod
    async def get_plant(plant_id: str) -> Optional[PlantSchema]:
        try:
            async with AsyncClient() as client:
                response = await client.get(PLANT_SERVICE_URL + f"/plants/{plant_id}")
                if response.status_code == codes.OK:
                    return PlantSchema(**response.json())
                elif response.status_code == codes.NOT_FOUND:
                    return None
                else:
                    return response.raise_for_status().json()
                    
        except Exception as e:
            logger.error(
                "Plant service cannot be accessed because: " + str(e)
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Plant service service cannot be accessed",
            )
