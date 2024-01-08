CREATE SCHEMA IF NOT EXISTS dev;

CREATE TABLE IF NOT EXISTS dev.device_plant (
    id_device VARCHAR(32) PRIMARY KEY,
    id_plant INT UNIQUE NOT NULL,
    plant_type SMALLINT NOT NULL,
    id_user INT NOT NULL
);

CREATE TABLE IF NOT EXISTS dev.measurements (
    id SERIAL PRIMARY KEY,
    id_plant INT,
    plant_type SMALLINT,
    time_stamp VARCHAR(50),
    temperature SMALLINT,
    humidity SMALLINT,
    light SMALLINT,
    watering SMALLINT
);

CREATE TABLE IF NOT EXISTS dev.numbers (
    number INT PRIMARY KEY
);