    CREATE SCHEMA IF NOT EXISTS measurements;
    CREATE TABLE
        IF NOT EXISTS measurements.device_plant (
            id_device VARCHAR(32) PRIMARY KEY,
            id_plant INT UNIQUE NOT NULL,
            plant_type SMALLINT NOT NULL,
            id_user INT NOT NULL
    );

    DO $do$ BEGIN
        IF (SELECT COUNT(*) FROM measurements.device_plant) = 0 THEN
            INSERT INTO measurements.device_plant (id_device, id_plant, plant_type, id_user) VALUES 
                ('fd7c7531467748539f99d2bcef076c88', 1, 1, 1),
                ('fd8c7531467748539f99d2bcef076c88', 2, 2, 2),
                ('fd9c7531467748539f99d2bcef076c88', 3, 3, 3);
        END IF;
    END $do$;