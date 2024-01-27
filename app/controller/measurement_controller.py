from controller.device_plant_controller import withSQLExceptionsHandle
from fastapi import Request

@withSQLExceptionsHandle
def last_measurement_made_by_plant(req: Request, id_plant: int):
    try:
        return req.app.database.get_last_measurement(id_plant)
    except Exception as err:
        req.app.database.rollback()
        raise err
