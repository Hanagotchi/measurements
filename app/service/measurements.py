from fastapi import status
from fastapi.responses import Response
from repository.measurements import MeasurementsRepository
from exceptions.MeasurementsException import PlantNotFound, UserUnauthorized
from schemas.measurement import MeasurementSavedSchema
from resources.rule_parser import apply_rules
from external.Plants import PlantsService
from external.Users import UsersService


class MeasurementsService:
    def __init__(
        self,
        measurements_repository: MeasurementsRepository,
        user_service: UsersService,
        plant_service: PlantsService
    ):
        self.measurements_repository = measurements_repository
        self.user_service = user_service
        self.plant_service = plant_service

    async def get_plant_last_measurement(self, id_plant, token):
        user_id = await self.user_service.get_user_id(token)
        owner_id = await self.__get_plant_owner(id_plant)
        if owner_id != user_id:
            raise UserUnauthorized
        last_measurement = \
            self.measurements_repository.get_plant_last_measurement(id_plant)
        if not last_measurement:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
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
        user_id = await self.user_service.get_user_id(token)
        plant_owner = await self.__get_plant_owner(plant.id)
        if plant_owner != user_id:
            raise UserUnauthorized
        try:
            device_plant = self.measurements_repository.\
                create_device_plant_relation(plant,
                                             device_plant)
            return device_plant
        except Exception as err:
            self.measurements_repository.rollback()
            raise err

    async def update_device_plant(self, id_device, plant_id, token):
        plant = await self.plant_service.get_plant(plant_id)
        if not plant:
            raise PlantNotFound(plant_id)

        user_id = await self.user_service.get_user_id(token)
        plant_owner = plant.id_user

        # User is not the new plant owner
        if plant_owner != user_id:
            raise UserUnauthorized

        # User is not the old plant owner
        old_device_plant = self.measurements_repository.\
            find_by_device_id(id_device)
        if old_device_plant['id_user'] != user_id:
            raise UserUnauthorized

        try:
            self.measurements_repository.\
                update_device_plant(id_device,
                                    plant.id,
                                    plant.scientific_name,
                                    plant.id_user)
            return self.measurements_repository.find_by_device_id(id_device)
        except Exception as err:
            self.measurements_repository.rollback()
            raise err

    async def get_device_plant(self,
                               token: str,
                               query_params: dict = None,
                               device_id: str = None):
        user_id = await self.user_service.get_user_id(token)
        if device_id:
            result = self.measurements_repository.find_by_device_id(device_id)
            if not result:
                return None
            if user_id != result["id_user"]:
                raise UserUnauthorized
            return result
        id_plant = query_params.get("id_plant")
        limit = query_params.get("limit")
        if id_plant:
            result = self.measurements_repository.find_by_plant_id(id_plant)
            if not result:
                return None
            if user_id != result["id_user"]:
                raise UserUnauthorized
            return result
        return self.measurements_repository.find_by_user_id(user_id, limit)

    async def delete_device_plant_relation(self, type_id, id, token: str):
        user_id = await self.user_service.get_user_id(token)
        if type_id == 'id_device':
            owner = self.measurements_repository.\
                find_by_device_id(id).get("id_user")
        else:
            owner = await self.__get_plant_owner(id)

        if owner != user_id:
            raise UserUnauthorized

        result_rowcount = self.measurements_repository.\
            delete_by_field(type_id, id)
        return result_rowcount if result_rowcount else None

    async def __get_plant_owner(self, plant_id: int) -> int:
        plant = await self.plant_service.get_plant(plant_id)
        return plant.id_user if plant else None
