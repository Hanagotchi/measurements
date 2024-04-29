from fastapi import status
from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
from service.measurements import MeasurementsService
from service.plants import PlantsService
from schemas.measurement import MeasurementSavedSchema


class MeasurementsController:
    def __init__(self, measurements_service: MeasurementsService,
                 plants_service: PlantsService):
        self.measurements_service = measurements_service
        self.plants_service = plants_service

    def handle_get_plant_last_measurement(self,
                                          id_plant: int) -> MeasurementSavedSchema:
        measurement = self.measurements_service.get_plant_last_measurement(id_plant)
        return measurement

    async def handle_create_device_plant_relation(self, device_plant: dict):
        plant_id = device_plant["id_plant"]
        plant = await self.plants_service.get_plant(plant_id)
        device_plant = self.measurements_service.create_device_plant_relation(
            plant,
            device_plant)
        if not device_plant:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "plant_id": (
                        "Could not found any plant "
                        f"with id {device_plant.get('id_plant')}"
                    )
                },
            )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=device_plant
        )

    async def handle_update_device_plant(self, id_device: str,
                                         update_device_plant_info: dict):
        plant_id = update_device_plant_info.get("id_plant")
        if not plant_id:
            device_plant = self.measurements_service.get_device_plant(
                id_device=id_device)
        else:
            plant = await self.plants_service.get_plant(
                update_device_plant_info.get("id_plant"))
            device_plant = self.measurements_service.update_device_plant(id_device,
                                                                         plant,
                                                                         plant_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=device_plant
        )

    def handle_get_device_plant(self, query_params: dict):
        device_plant = self.measurements_service.get_device_plant(
            query_params=query_params)
        if not device_plant:
            return JSONResponse(
                status_code=status.HTTP_204_NO_CONTENT,
                content={}
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=device_plant
        )

    def handle_delete_device_plant_relation(self, type_id, id):
        response = self.measurements_service.delete_device_plant_relation(type_id, id)
        if response:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response
                )
        return JSONResponse(
                status_code=status.HTTP_204_NO_CONTENT,
                content={}
            )
