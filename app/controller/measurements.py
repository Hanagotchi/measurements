from service.measurements import MeasurementsService
from service.plants import PlantsService
from schemas.measurement import MeasurementSavedSchema


class MeasurementsController:
    def __init__(self, measurements_service: MeasurementsService,
                 plants_service: PlantsService):
        self.measurements_service = measurements_service

    def handle_get_plant_last_measurement(self,
                                          id_plant: int) -> MeasurementSavedSchema:
        measurement = self.measurements_service.get_plant_last_measurement(id_plant)
        return measurement

    async def handle_create_device_plant_relation(self, device_plant: dict):
        plant_id = device_plant["id_plant"]
        plant = await self.plants_service.get_plant(plant_id)
        return self.measurements_service.create_device_plant_relation(plant,
                                                                      device_plant)

    def create_measurement(self, request):
        return self.measurements_service.create_measurement(request)

    def update_measurement(self, request):
        return self.measurements_service.update_measurement(request)

    def delete_measurement(self, request):
        return self.measurements_service.delete_measurement(request)
