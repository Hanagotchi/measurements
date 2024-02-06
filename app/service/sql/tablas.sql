CREATE SCHEMA IF NOT EXISTS dev;

CREATE TABLE
    IF NOT EXISTS dev.device_plant (
        id_device VARCHAR(32) PRIMARY KEY,
        id_plant INT UNIQUE NOT NULL,
        plant_type SMALLINT NOT NULL,
        id_user INT NOT NULL
    );

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

CREATE TABLE IF NOT EXISTS numbers (number INT PRIMARY KEY);