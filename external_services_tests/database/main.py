from tests import test_DB_device_plant, test_DB_measurements
from sql_alchemy import SQL_Alchemy

test_DB_device_plant(SQL_Alchemy())
test_DB_measurements(SQL_Alchemy())