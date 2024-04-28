from repository.measurements import MeasurementsRepository


class MeasurementsService:
    def __init__(self, measurements_repository: MeasurementsRepository):
        self.measurements_repository = measurements_repository

    def get_plant_last_measurement(self, id_plant):
        return self.measurements_repository.get_plant_last_measurement(id_plant)

    def get_measurement(self, request):
        return self.measurements_repository.get_measurement(request)

    def create_measurement(self, request):
        return self.measurements_repository.create_measurement(request)

    def update_measurement(self, request):
        return self.measurements_repository.update_measurement(request)

    def delete_measurement(self, request):
        return self.measurements_repository.delete_measurement(request)