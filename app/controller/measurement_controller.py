from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from controller.device_plant_controller import withSQLExceptionsHandle
from fastapi import Request, status

from resources.parser import apply_rules
from schemas.measurement import MeasurementSavedSchema
from sqlalchemy.exc import NoResultFound


@withSQLExceptionsHandle(async_mode=False)
def last_measurement_made_by_plant(req: Request, id_plant: int):
    try:
        last_measurement = MeasurementSavedSchema.model_validate(
            req.app.database.get_last_measurement(id_plant).__dict__
        )
        last_measurement.deviations = apply_rules(
            last_measurement,
            last_measurement.plant_type
        )
        return last_measurement

    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content=jsonable_encoder([])
        )

    except Exception as err:
        req.app.database.rollback()
        raise err
