#!/bin/bash

set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "measurements" <<-'EOSQL'
    CREATE SCHEMA IF NOT EXISTS dev;
    CREATE TABLE
        IF NOT EXISTS dev.measurements (
            id SERIAL PRIMARY KEY,
            id_plant INT,
            plant_type SMALLINT,
            time_stamp VARCHAR(50),
            temperature SMALLINT,
            humidity SMALLINT CHECK (
                humidity >= 0
                AND humidity <= 100
            ),
            light SMALLINT CHECK (light >= 0),
            watering SMALLINT CHECK (
                watering >= 0
                AND watering <= 100
            )
        );
EOSQL