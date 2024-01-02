""" from postgres import Postgres
from tests import test_DB

test_DB(Postgres()) """

from sql_alchemy import SQL_Alchemy

sql = SQL_Alchemy()
sql.shutdown()