from fastapi import Request, status, HTTPException
from database.models.device_plant import DevicePlant
from schemas.device_plant import DevicePlantSchema, DevicePlantUpdateSchema
import logging
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import PendingRollbackError, IntegrityError
from typing import Union


logger = logging.getLogger("app")
logger.setLevel("DEBUG")


def create_device_plant_relation(req: Request, device_plant: DevicePlantSchema):
    try:
        req.app.database.add_new(DevicePlant.from_pydantic(device_plant))
        return req.app.database.find_device_plant(device_plant.id_device)
    except IntegrityError as err:
        req.app.database.rollback()

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
        req.app.database.rollback()
        logger.warning(format(err))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=format(err))


def update_device_plant(req: Request,
                        device_plant_update_set: Union[
                            DevicePlantSchema,
                            DevicePlantUpdateSchema
                            ]):
    try:
        req.app.database.update_device_plant(
            device_plant_update_set.id_device,
            device_plant_update_set.id_plant,
            device_plant_update_set.plant_type,
            device_plant_update_set.id_user,
        )
        return req.app.database.find_device_plant(device_plant_update_set.id_device)
    except IntegrityError as err:
        req.app.database.rollback()

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
        req.app.database.rollback()
        logger.warning(format(err))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=format(err))
