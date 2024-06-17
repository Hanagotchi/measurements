from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from service.measurements import MeasurementsService
from external.Plants import PlantsService
from schemas.measurement import MeasurementSavedSchema


class MeasurementsController:
    def __init__(self, measurements_service: MeasurementsService,
                 plants_service: PlantsService):
        self.measurements_service = measurements_service
        self.plants_service = plants_service

    async def handle_get_plant_last_measurement(self,
                                                id_plant: int,
                                                token: str
                                                ) -> MeasurementSavedSchema:
        measurement = await self.\
            measurements_service.get_plant_last_measurement(id_plant, token)
        return measurement

    async def handle_create_device_plant_relation(self,
                                                  device_plant: dict,
                                                  token: str):
        plant_id = device_plant.get("id_plant")
        plant = await self.plants_service.get_plant(plant_id)
        device_plant = await self.\
            measurements_service.create_device_plant_relation(plant,
                                                              device_plant,
                                                              token)
        if not device_plant:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "plant_id": (
                        "Could not find any plant"
                    )
                },
            )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=device_plant
        )

    async def handle_update_device_plant(self, id_device: str,
                                         update_device_plant_info: dict,
                                         token: str):

        plant_id = update_device_plant_info.get("id_plant")
        if not plant_id:
            device_plant = await self.measurements_service.get_device_plant(
                token, device_id=id_device)
        else:
            device_plant = await self.measurements_service.update_device_plant(
                id_device, plant_id, token)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=device_plant
        )

    async def handle_get_device_plant(self, query_params: dict, token: str):
        device_plant = await self.measurements_service.get_device_plant(
            token, query_params=query_params)
        if not device_plant:
            return JSONResponse(
                status_code=status.HTTP_204_NO_CONTENT,
                content={}
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=device_plant
        )

    async def handle_delete_device_plant_relation(self,
                                                  type_id,
                                                  id,
                                                  token: str):
        response = await self.measurements_service.\
            delete_device_plant_relation(type_id,
                                         id,
                                         token)
        if response:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=jsonable_encoder({
                    "message": "Device plant relation deleted successfully.",
                    }),
                )
        return JSONResponse(
                status_code=status.HTTP_204_NO_CONTENT,
                content={}
            )
