-- SQLBook: Code
CREATE SCHEMA IF NOT EXISTS my_scheme;

CREATE TABLE IF NOT EXISTS my_scheme.usuarios(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    email VARCHAR(100)
);

-- Para probar :D
-- INSERT INTO my_scheme.usuarios (nombre, email) VALUES
--     ('Juan', 'juan@example.com'),
--     ('María', 'maria@example.com');

-- SELECT * FROM my_scheme.usuarios;
