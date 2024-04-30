from fastapi import status
from fastapi.responses import JSONResponse
from repository.measurements import MeasurementsRepository
from exceptions.MeasurementsException import PlantNotFound
from schemas.measurement import MeasurementSavedSchema
from resources.parser import apply_rules


class MeasurementsService:
    def __init__(self, measurements_repository: MeasurementsRepository):
        self.measurements_repository = measurements_repository

    def get_plant_last_measurement(self, id_plant):
        last_measurement = self.measurements_repository.get_plant_last_measurement(
            id_plant)
        if not last_measurement:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
        last_measurement = MeasurementSavedSchema.model_validate(
            last_measurement.__dict__)
        last_measurement.deviations = apply_rules(
            last_measurement,
            last_measurement.plant_type
        )
        return last_measurement

    def create_device_plant_relation(self, plant, device_plant):
        if not plant:
            return None
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
            raise PlantNotFound(plant_id)
        try:
            self.measurements_repository.update_device_plant(id_device,
                                                             plant.id,
                                                             plant.scientific_name,
                                                             plant.id_user)
            return self.measurements_repository.find_by_device_id(id_device)
        except Exception as err:
            self.measurements_repository.rollback()
            raise err

    def get_device_plant(self, query_params: dict = None, device_id: str = None):
        if device_id:
            return self.measurements_repository.find_by_device_id(device_id)
        id_plant = query_params.get("id_plant", None)
        limit = query_params.get("limit")
        if id_plant:
            result = self.measurements_repository.find_by_plant_id(id_plant)
            return result
        return self.measurements_repository.find_all(limit)

    def delete_device_plant_relation(self, type_id, id):
        result_rowcount = 0
        if type_id == "id_device":
            result_rowcount = self.measurements_repository.delete_by_field(type_id, id)
        else:
            result_rowcount = self.measurements_repository.delete_by_field(type_id, id)

        return result_rowcount if result_rowcount else None
