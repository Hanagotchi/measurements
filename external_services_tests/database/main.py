#from mongo import Mongo
from postgres import Postgres

from tests import test_DB


test_DB(Postgres())