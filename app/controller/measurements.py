from fastapi import status
from service.measurements import MeasurementsService


class MeasurementsController:
    def __init__(self, measurements_service: MeasurementsService):
        self.measurements_service = measurements_service

    def handle_get_plant_last_measurement(self, id_plant):
        measurement = self.measurements_service.get_plant_last_measurement(id_plant)
        return {"message": measurement, "status": status.HTTP_200_OK}

    def get_measurement(self, request):
        return self.measurements_service.get_measurement(request)

    def create_measurement(self, request):
        return self.measurements_service.create_measurement(request)

    def update_measurement(self, request):
        return self.measurements_service.update_measurement(request)

    def delete_measurement(self, request):
        return self.measurements_service.delete_measurement(request)