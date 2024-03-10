from typing import Literal, Union
from fastapi import Response, Request, status, HTTPException
from database.models.device_plant import DevicePlant
from schemas.device_plant import (
    DevicePlantCreateSchema,
    DevicePlantPartialUpdateSchema,
    DevicePlantUpdateSchema,
)
import logging
from sqlalchemy.exc import PendingRollbackError, IntegrityError, NoResultFound
from fastapi.responses import JSONResponse
from service.plant_service import PlantService

logger = logging.getLogger("app")
logger.setLevel("DEBUG")


def handle_common_errors(err):

    if isinstance(err, IntegrityError):
        parsed_error = err.orig.pgerror.split("\n")[1]
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=parsed_error,
        )

    if isinstance(err, PendingRollbackError):
        logger.warning(format(err))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=format(err)
        )

    if isinstance(err, NoResultFound):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=format(err)
        )

    logger.error(format(err))
    print("Holi", err)
    raise err

    """logger.error(format(err))
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=format(err)
    ) """


def withSQLExceptionsHandle(async_mode: bool):

    def decorator(func):
        async def handleAsyncSQLException(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as err:
                return handle_common_errors(err)

        def handleSyncSQLException(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as err:
                return handle_common_errors(err)

        return (
            handleAsyncSQLException if async_mode else handleSyncSQLException
        )

    return decorator


@withSQLExceptionsHandle(async_mode=True)
async def create_device_plant_relation(
    req: Request, device_plant: DevicePlantCreateSchema
):
    try:
        plant = await PlantService.get_plant(device_plant.id_plant)
        if not plant:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "plant_id": (
                        "Could not found any plant "
                        f"with id {device_plant.id_plant}"
                    )
                },
            )

        plant_type = await PlantService.get_plant_type(plant.scientific_name)
        if not plant_type:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "scientific_name": (
                        "Could not found any plant type "
                        f"with scientific name {plant.scientific_name}"
                    )
                },
            )

        device_plant = DevicePlant(
            id_device=device_plant.id_device,
            id_plant=device_plant.id_plant,
            plant_type=plant_type.id,
            id_user=plant.id_user,
        )  # type: ignore
        req.app.database.add(device_plant)
        return device_plant

    except Exception as err:
        req.app.database.rollback()
        raise err


@withSQLExceptionsHandle(async_mode=True)
async def update_device_plant(
    req: Request,
    id_device: str,
    device_plant_update_set: Union[
        DevicePlantUpdateSchema, DevicePlantPartialUpdateSchema
    ],
):
    try:
        if not device_plant_update_set.id_plant:
            return req.app.database.find_by_device_id(id_device)

        plant = await PlantService.get_plant(device_plant_update_set.id_plant)
        if not plant:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "plant_id": (
                        "Could not found any plant with "
                        f"id {device_plant_update_set.id_plant}"
                    )
                },
            )

        plant_type = await PlantService.get_plant_type(plant.scientific_name)
        if not plant_type:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "scientific_name": (
                        "Could not found any plant type "
                        f"with scientific name {plant.scientific_name}"
                    )
                },
            )

        req.app.database.update_device_plant(
            id_device,
            plant.id,
            plant_type.id,
            plant.id_user,
        )
        return req.app.database.find_by_device_id(id_device)
    except Exception as err:
        req.app.database.rollback()
        raise err


@withSQLExceptionsHandle(async_mode=False)
def get_device_plant_relation(req: Request, id_plant: int):
    return req.app.database.find_by_plant_id(id_plant)


@withSQLExceptionsHandle(async_mode=False)
def get_all_device_plant_relations(req: Request, limit: int):
    return req.app.database.find_all(limit)


@withSQLExceptionsHandle(async_mode=False)
def delete_device_plant_relation(
    req: Request,
    response: Response,
    type_id: Literal["id_device", "id_plant"],
    id: str
):
    result_rowcount = 0
    if type_id == "id_device":
        result_rowcount = req.app.database.delete_by_field(type_id, id)
    else:
        result_rowcount = req.app.database.delete_by_field(type_id, id)

    if result_rowcount == 0:
        response.status_code = status.HTTP_204_NO_CONTENT
        return  # EMPTY RESPONSE! RESOURCE DID NOT EXIST
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"deleted": "Device-plant relation deleted successfully"},
        )
