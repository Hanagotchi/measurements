from typing import Union
from fastapi import Request, status, HTTPException
from database.models.device_plant import DevicePlant
from schemas.device_plant import (
    DevicePlantPartialUpdateSchema,
    DevicePlantSchema,
    DevicePlantUpdateSchema
)
import logging
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import PendingRollbackError, IntegrityError, NoResultFound

logger = logging.getLogger("app")
logger.setLevel("DEBUG")


def withSQLExceptionsHandle(func):
    def handleSQLException(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                parsed_error = err.orig.pgerror.split("\n")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error": parsed_error[0],
                        "detail": parsed_error[1]
                    })

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=format(err))

        except PendingRollbackError as err:
            logger.warning(format(err))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=format(err))

        except NoResultFound as err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=format(err))

    return handleSQLException


@withSQLExceptionsHandle
def create_device_plant_relation(req: Request, device_plant: DevicePlantSchema):
    try:
        req.app.database.add(DevicePlant.from_pydantic(device_plant))
        return req.app.database.find_by_device_id(device_plant.id_device)
    except Exception as err:
        req.app.database.rollback()
        raise err


@withSQLExceptionsHandle
def update_device_plant(req: Request,
                        id_device: str,
                        device_plant_update_set:
                        Union[DevicePlantUpdateSchema, DevicePlantPartialUpdateSchema]):
    try:
        req.app.database.update_device_plant(
            id_device,
            device_plant_update_set.id_plant,
            device_plant_update_set.plant_type,
            device_plant_update_set.id_user,
        )
        return req.app.database.find_by_device_id(id_device)
    except Exception as err:
        req.app.database.rollback()
        raise err


@withSQLExceptionsHandle
def get_device_plant_relation(req: Request, id_plant: str):
    return req.app.database.find_by_plant_id(id_plant)


@withSQLExceptionsHandle
def get_all_device_plant_relations(req: Request):
    return req.app.database.find_all()
