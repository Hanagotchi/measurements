#!/bin/bash

set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$MEASUREMENTS_DB" <<-'EOSQL'
    CREATE SCHEMA IF NOT EXISTS dev;
    CREATE TABLE
        IF NOT EXISTS dev.device_plant (
            id_device VARCHAR(32) PRIMARY KEY,
            id_plant INT UNIQUE NOT NULL,
            plant_type VARCHAR(70) NOT NULL,
            id_user INT NOT NULL
    );

    DO $do$ BEGIN
        IF (SELECT COUNT(*) FROM dev.device_plant) = 0 THEN
            INSERT INTO dev.device_plant (id_device, id_plant, plant_type, id_user) VALUES 
                ('fd7c7531467748539f99d2bcef076c88', 1, 'Passiflora caerulea', 1),
                ('fd8c7531467748539f99d2bcef076c88', 2, 'Kalanchoe daigremontiana', 2),
                ('fd9c7531467748539f99d2bcef076c88', 3, 'Dracaena fragrans', 3);
        END IF;
    END $do$;
EOSQL