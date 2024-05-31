from fastapi import status
from fastapi.responses import JSONResponse
from repository.measurements import MeasurementsRepository
from exceptions.MeasurementsException import PlantNotFound, UserUnauthorized
from schemas.measurement import MeasurementSavedSchema
from resources.parser import apply_rules
from external.Users import UsersService
from external.Plants import PlantsService


class MeasurementsService:
    def __init__(self, measurements_repository: MeasurementsRepository):
        self.measurements_repository = measurements_repository

    async def get_plant_last_measurement(self, id_plant, token):
        user_id = await UsersService.get_user_id(token)
        owner_id = await self.__get_plant_owner(id_plant)
        if owner_id != user_id:
            raise UserUnauthorized
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

    async def create_device_plant_relation(self, plant, device_plant, token):
        if not plant:
            return None
        user_id = await UsersService.get_user_id(token)
        plant_owner = await self.__get_plant_owner(plant.id)
        if plant_owner != user_id:
            raise UserUnauthorized
        try:
            device_plant = self.measurements_repository.create_device_plant_relation(
                plant, device_plant
                )
            return device_plant
        except Exception as err:
            self.measurements_repository.rollback()
            raise err

    async def update_device_plant(self, id_device, plant, plant_id, token):
        user_id = await UsersService.get_user_id(token)
        plant_owner = await self.__get_plant_owner(plant_id)
        print(f"plant_owner: {plant_owner}, user_id: {user_id}")
        if plant_owner != user_id:
            raise UserUnauthorized
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

    async def get_device_plant(self, token: str, query_params: dict = None,
                               device_id: str = None):
        user_id = await UsersService.get_user_id(token)
        if device_id:
            result = self.measurements_repository.find_by_device_id(device_id)
            print(f"user_id: {user_id}, result: {result['id_user']}")
            if user_id != result.get("id_user"):
                raise UserUnauthorized
            return result
        id_plant = query_params.get("id_plant", None)
        limit = query_params.get("limit")
        if id_plant:
            result = self.measurements_repository.find_by_plant_id(id_plant)
            if user_id != result.get("id_user"):
                raise UserUnauthorized
            return result
        return self.measurements_repository.find_by_user_id(user_id, limit)

    def delete_device_plant_relation(self, type_id, id):
        result_rowcount = 0
        if type_id == "id_device":
            result_rowcount = self.measurements_repository.delete_by_field(type_id, id)
        else:
            result_rowcount = self.measurements_repository.delete_by_field(type_id, id)

        return result_rowcount if result_rowcount else None

    async def __get_plant_owner(self, plant_id: int) -> int:
        plant = await PlantsService.get_plant(plant_id)
        return plant.id_user if plant else None
