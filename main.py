from database.mongo import Mongo
from database.postgres import Postgres

from service_tests.database.test import test_DB


test_DB(Postgres())