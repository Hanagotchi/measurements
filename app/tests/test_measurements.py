import pytest
import unittest
from datetime import datetime
from mock import Mock, MagicMock
from repository.measurements import MeasurementsRepository
from service.measurements import MeasurementsService
from external.Users import UsersService
from external.Plants import PlantsService
from database.models.device_plant import DevicePlant
from schemas.plant import PlantSchema
from models.measurement import Measurement

device_plant = {
    "id_device": "ax-ex",
    "id_plant": 16,
    "plant_type": "Thunbergia alata",
    "id_user": 2
}

device_plant2 = {
    "id_device": "ar-exg5",
    "id_plant": 13,
    "plant_type": "Thunbergia alata",
    "id_user": 2
}

plant = PlantSchema(
    id=16,
    name="Planta",
    scientific_name="Thunbergia alata",
    id_user=2
)


measurement = Measurement(
    id_plant=1,
    plant_type="Thunbergia alata",
    time_stamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    temperature=24.5,
    humidity=55,
    light=300.0,
    watering=20
)

token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ8.eyJ1c2VyX2lkLjo5fQ.qRPlwqqpK30CXwiE5AusCqELWUwH6NRpiTiOGxUrIZK'


class ServiceTests(unittest.IsolatedAsyncioTestCase):

    def _getMock(self, classToMock, attributes=None):
        if attributes is None:
            attributes = {}
        mock = MagicMock(spec=classToMock)
        mock.configure_mock(**attributes)
        return mock

    async def test_get_device_plant_by_user(self):
        attr_db = {
            "find_by_user_id.return_value": [device_plant, device_plant2],
        }
        mock_db = self._getMock(MeasurementsRepository, attr_db)

        attr_user = {
            "get_user_id.return_value": 2
        }
        mock_user = self._getMock(UsersService, attr_user)

        service = MeasurementsService(mock_db, mock_user, Mock())
        result = await service.get_device_plant(token=token)

        self.assertEqual(len(result), 2)
        mock_db.find_by_user_id.assert_called_once()

    async def test_get_device_plant_by_device_id(self):
        attr_db = {
            "find_by_device_id.return_value": device_plant,
        }
        mock_db = self._getMock(MeasurementsRepository, attr_db)

        attr_user = {
            "get_user_id.return_value": 2
        }
        mock_user = self._getMock(UsersService, attr_user)

        service = MeasurementsService(mock_db, mock_user, Mock())
        result = await service.get_device_plant(token=token, device_id="ax-ex")

        self.assertEqual(result, device_plant)
        mock_db.find_by_device_id.assert_called_once()

    async def test_get_device_plant_by_plant_id(self):
        attr_db = {
            "find_by_plant_id.return_value": device_plant,
        }
        mock_db = self._getMock(MeasurementsRepository, attr_db)

        attr_user = {
            "get_user_id.return_value": 2
        }
        mock_user = self._getMock(UsersService, attr_user)

        service = MeasurementsService(mock_db, mock_user, Mock())
        result = await service.get_device_plant(token=token, query_params={'id_plant': 16})

        self.assertEqual(result, device_plant)
        mock_db.find_by_plant_id.assert_called_once()

    async def test_get_last_measurement(self):
        attr_db = {
            "get_plant_last_measurement.return_value": measurement,
        }
        mock_db = self._getMock(MeasurementsRepository, attr_db)

        attr_user = {
            "get_user_id.return_value": 2
        }
        mock_user = self._getMock(UsersService, attr_user)

        attr_plants = {
            "get_plant.return_value": plant
        }
        mock_plants = self._getMock(PlantsService, attr_plants)

        service = MeasurementsService(mock_db, mock_user, mock_plants)
        result = await service.get_plant_last_measurement(id_plant=16, token=token)

        self.assertEqual(result, measurement)
        mock_db.get_plant_last_measurement.assert_called_once()


    
    
