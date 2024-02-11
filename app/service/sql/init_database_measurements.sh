#!/bin/bash

set -e
set -u

echo "  Creating user and database '$MEASUREMENTS_DB' "
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
	CREATE DATABASE "$MEASUREMENTS_DB";
	GRANT ALL PRIVILEGES ON DATABASE "$MEASUREMENTS_DB" TO "$POSTGRES_USER";
EOSQL