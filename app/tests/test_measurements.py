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
from pydantic import ValidationError
from schemas.measurement import MeasurementSavedSchema
from exceptions.MeasurementsException import PlantNotFound, UserUnauthorized

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

measurement = MeasurementSavedSchema(
    id=1221,
    id_plant=16,
    plant_type="Thunbergia alata",
    time_stamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    temperature=20.5,
    humidity=55,
    light=350.0,
    watering=60
)

token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ8.eyJ1c2VyX2lkLjo5fQ.qRPlwqqpK30CXwiE5AusCqELWUwH6NRpiTiOGxUrIZK'


class ServiceTests(unittest.IsolatedAsyncioTestCase):

    def _getMock(self, classToMock, attributes=None):
        if attributes is None:
            attributes = {}
        mock = MagicMock(spec=classToMock)
        mock.configure_mock(**attributes)
        return mock

    async def test_get_device_plant_by_user_id(self):
        attr_db = {
            "find_by_user_id.return_value": [device_plant, device_plant2],
        }
        mock_db = self._getMock(MeasurementsRepository, attr_db)

        attr_user = {
            "get_user_id.return_value": 2
        }
        mock_user = self._getMock(UsersService, attr_user)

        service = MeasurementsService(mock_db, mock_user, Mock())
        result = await service.get_device_plant(token=token, query_params={'id_plant': None})

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
    
    async def test_get_unauthorized_device_plant_by_device_id(self):
        attr_db = {
            "find_by_device_id.return_value": device_plant,
        }
        mock_db = self._getMock(MeasurementsRepository, attr_db)

        attr_user = {
            "get_user_id.return_value": 8
        }
        mock_user = self._getMock(UsersService, attr_user)

        service = MeasurementsService(mock_db, mock_user, Mock())

        with self.assertRaises(UserUnauthorized):
            await service.get_device_plant(token=token, device_id="ax-ex")

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

    async def test_get_unauthorized_device_plant_by_plant_id(self):
        attr_db = {
            "find_by_plant_id.return_value": device_plant,
        }
        mock_db = self._getMock(MeasurementsRepository, attr_db)

        attr_user = {
            "get_user_id.return_value": 8
        }
        mock_user = self._getMock(UsersService, attr_user)

        service = MeasurementsService(mock_db, mock_user, Mock())

        with self.assertRaises(UserUnauthorized):
            await service.get_device_plant(token=token, query_params={'id_plant': 16})

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

        self.assertEqual(result.id_plant, measurement.id_plant)
        self.assertTrue(result.deviations.hasDeviations)
        mock_db.get_plant_last_measurement.assert_called_once()
    
    async def test_get_last_measurement_unauthorized(self):
        attr_plants = {
            "get_plant.return_value": plant
        }
        mock_plants = self._getMock(PlantsService, attr_plants)

        attr_user = {
            "get_user_id.return_value": 8
        }
        mock_user = self._getMock(UsersService, attr_user)

        service = MeasurementsService(Mock(), mock_user, mock_plants)

        with self.assertRaises(UserUnauthorized):
            await service.get_plant_last_measurement(id_plant=16, token=token)

    async def test_create_device_plant(self):
        attr_db = {
            "create_device_plant_relation.return_value": device_plant,
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
        result = await service.create_device_plant_relation(token=token, plant=plant, device_plant=device_plant)

        self.assertEqual(result, device_plant)
        mock_db.create_device_plant_relation.assert_called_once()
    
    async def test_create_unauthorized_device_plant(self):
        attr_plants = {
            "get_plant.return_value": plant
        }
        mock_plants = self._getMock(PlantsService, attr_plants)

        attr_user = {
            "get_user_id.return_value": 8
        }
        mock_user = self._getMock(UsersService, attr_user)

        service = MeasurementsService(Mock(), mock_user, mock_plants)

        with self.assertRaises(UserUnauthorized):
            await service.create_device_plant_relation(token=token, plant=plant, device_plant=device_plant) 
    
    async def test_create_device_plant_raises_exception(self):
        attr_db = {
            "create_device_plant_relation.side_effect": Exception(),
            "rollback.return_value": None
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

        with self.assertRaises(Exception):
            result = await service.create_device_plant_relation(token=token, plant=plant, device_plant=device_plant)

        mock_db.rollback.assert_called_once()
        mock_db.create_device_plant_relation.assert_called_once()
        
    async def test_update_nonexisting_device_plant(self):
        attr_plants = {
            "get_plant.return_value": None
        }
        mock_plants = self._getMock(PlantsService, attr_plants)

        service = MeasurementsService(Mock(), Mock(), mock_plants)

        with self.assertRaises(PlantNotFound):
            await service.update_device_plant(token=token, id_device="ax-ex", plant_id=10)

    async def test_update_unauthorized_device_plant(self):
        attr_plants = {
            "get_plant.return_value": plant
        }
        mock_plants = self._getMock(PlantsService, attr_plants)

        attr_user = {
            "get_user_id.return_value": 8
        }
        mock_user = self._getMock(UsersService, attr_user)

        service = MeasurementsService(Mock(), mock_user, mock_plants)

        with self.assertRaises(UserUnauthorized):
            await service.update_device_plant(token=token, id_device="ax-ex", plant_id=16)
    
    async def test_update_device_plant(self):
        attr_db = {
            "find_by_device_id.return_value": device_plant
        }
        mock_db = self._getMock(MeasurementsRepository, attr_db)

        attr_plants = {
            "get_plant.return_value": plant
        }
        mock_plants = self._getMock(PlantsService, attr_plants)

        attr_user = {
            "get_user_id.return_value": 2
        }
        mock_user = self._getMock(UsersService, attr_user)

        service = MeasurementsService(mock_db, mock_user, mock_plants)
        result = await service.update_device_plant(token=token, id_device="a4x-he", plant_id=16)

        self.assertEqual(result, device_plant)
        mock_db.update_device_plant.assert_called_once()

    async def test_update_device_plant_raises_exception(self):
        attr_db = {
            "find_by_device_id.return_value": device_plant,
            "update_device_plant.side_effect": Exception(),
            "rollback.return_value": None
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

        with self.assertRaises(Exception):
            result = await service.update_device_plant(token=token, id_device="a4x-he", plant_id=16)

        mock_db.rollback.assert_called_once()
        mock_db.update_device_plant.assert_called_once()

    async def test_delete_device_plant_by_device_id(self):
        attr_db = {
            "find_by_device_id.return_value": device_plant,
            "delete_by_field.return_value": 1
        }
        mock_db = self._getMock(MeasurementsRepository, attr_db)

        attr_user = {
            "get_user_id.return_value": 2
        }
        mock_user = self._getMock(UsersService, attr_user)

        service = MeasurementsService(mock_db, mock_user, Mock())
        result = await service.delete_device_plant_relation(token=token, type_id="id_device", id="ax-ex")

        self.assertEqual(result, 1)
        mock_db.delete_by_field.assert_called_once()
    
    async def test_delete_device_plant_by_device_id(self):
        attr_db = {
            "find_by_device_id.return_value": device_plant,
            "delete_by_field.return_value": 1
        }
        mock_db = self._getMock(MeasurementsRepository, attr_db)

        attr_user = {
            "get_user_id.return_value": 2
        }
        mock_user = self._getMock(UsersService, attr_user)

        service = MeasurementsService(mock_db, mock_user, Mock())
        result = await service.delete_device_plant_relation(token=token, type_id="id_device", id="ax-ex")

        self.assertEqual(result, 1)
        mock_db.delete_by_field.assert_called_once()
    
    async def test_delete_device_plant_by_plant_id(self):
        attr_db = {
            "find_by_device_id.return_value": device_plant,
            "delete_by_field.return_value": 1
        }
        mock_db = self._getMock(MeasurementsRepository, attr_db)

        attr_plants = {
            "get_plant.return_value": plant
        }
        mock_plants = self._getMock(PlantsService, attr_plants)

        attr_user = {
            "get_user_id.return_value": 5
        }
        mock_user = self._getMock(UsersService, attr_user)

        service = MeasurementsService(mock_db, mock_user, mock_plants)
        with self.assertRaises(UserUnauthorized):
            await service.delete_device_plant_relation(token=token, type_id="id_plant", id=13)
    
    async def test_delete_unauthorized_device_plant_by_plant_id(self):
        attr_db = {
            "find_by_device_id.return_value": device_plant,
            "delete_by_field.return_value": 1
        }
        mock_db = self._getMock(MeasurementsRepository, attr_db)

        attr_plants = {
            "get_plant.return_value": plant
        }
        mock_plants = self._getMock(PlantsService, attr_plants)

        attr_user = {
            "get_user_id.return_value": 5
        }
        mock_user = self._getMock(UsersService, attr_user)

        service = MeasurementsService(mock_db, mock_user, mock_plants)
        with self.assertRaises(UserUnauthorized):
            await service.delete_device_plant_relation(token=token, type_id="id_plant", id=13)

