    CREATE SCHEMA IF NOT EXISTS measurements_service;
    CREATE TABLE
        IF NOT EXISTS measurements_service.measurements (
            id SERIAL PRIMARY KEY,
            id_plant INT,
            plant_type VARCHAR(70),
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