from fastapi import Request, Response, status, HTTPException
from database.models.device_plant import DevicePlant
from schemas.device_plant import DevicePlantSchema
import logging
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import PendingRollbackError, IntegrityError

logger = logging.getLogger("app")
logger.setLevel("DEBUG")


def create_device_plant_relation(req: Request, device_plant: DevicePlantSchema):
    try:
        req.app.database.add_new(DevicePlant.from_pydantic(device_plant))
        return req.app.database.find_device_plant(device_plant.id_device)
    except IntegrityError as err:
        req.app.database.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=format(err))
    except PendingRollbackError as err:
        req.app.database.rollback()
        logger.warning(format(err))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=format(err))