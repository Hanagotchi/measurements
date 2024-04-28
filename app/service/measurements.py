from fastapi import status
from fastapi.responses import JSONResponse
from repository.measurements import MeasurementsRepository


class MeasurementsService:
    def __init__(self, measurements_repository: MeasurementsRepository):
        self.measurements_repository = measurements_repository

    def get_plant_last_measurement(self, id_plant):
        return self.measurements_repository.get_plant_last_measurement(id_plant)

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

    def create_measurement(self, request):
        return self.measurements_repository.create_measurement(request)

    def update_measurement(self, request):
        return self.measurements_repository.update_measurement(request)

    def delete_measurement(self, request):
        return self.measurements_repository.delete_measurement(request)