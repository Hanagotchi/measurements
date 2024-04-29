from fastapi import status
from fastapi.responses import JSONResponse
from repository.measurements import MeasurementsRepository
from exceptions.MeasurementsException import PlantNotFound


class MeasurementsService:
    def __init__(self, measurements_repository: MeasurementsRepository):
        self.measurements_repository = measurements_repository

    def get_plant_last_measurement(self, id_plant):
        last_measurement = self.measurements_repository.get_plant_last_measurement(
            id_plant)
        print(f"last_measurement: {last_measurement}")
        if not last_measurement:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
        return last_measurement

    def create_device_plant_relation(self, plant, device_plant):
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
        try:
            device_plant = self.measurements_repository.create_device_plant_relation(
                plant, device_plant
                )
            return device_plant
        except Exception as err:
            self.measurements_repository.rollback()
            raise err

    def update_device_plant(self, id_device, plant, plant_id):
        if not plant:
            raise PlantNotFound(id)
        try:
            self.measurements_repository.update_device_plant(id_device,
                                                             plant.id,
                                                             plant.scientific_name,
                                                             plant.id_user)
            return self.measurements_repository.find_by_device_id(id_device)
        except Exception as err:
            self.measurements_repository.rollback()
            raise err

    def get_device_plant(self, query_params):
        id_plant = query_params.get("id_plant", None)
        limit = query_params.get("limit")
        if id_plant:
            result = self.measurements_repository.find_by_plant_id(id_plant)
            print(f"result: {result}")
            return result
        return self.measurements_repository.find_all(limit)
