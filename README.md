# Measurements Microservice

## Documentation

### .env structure

POSTGRES_USER: username to access the database (pick anyone. i.e: testuser)
POSTGRES_PASSWORD: password to access the database (pick anyone. i.e: test1234)
POSTGRES_DB: "measurements"
POSTGRES_HOST: localhost
POSTGRES_PORT: 5432

## Docker

#### Build container

```$ docker-compose build```

#### Start services

```$ docker-compose up```

#### List images

```$ docker images```

#### Remove dangling images: 

When you run a docker-compose build, it creates a new image, but it doesn't remove the old one, so you can have a lot of images with the same name but different id. Then, you can remove all of them with the following command:

```$ docker rmi $(docker images -f dangling=true -q) -f```

#### Deep Cleaning - Free space on your disk
*Warning*: This will remove all containers, images, volumes and networks not used by at least one container.
Its *recommended* to run this command before docker-compose up to avoid problems.

```$ docker system prune -a --volumes```

## RabbitMQ

#### Test it

Requires pika

To launch publisher

``` $ python3 /external_services_tests/rabbitmq/sender.py ```

To launch consumer

``` $ python3 /external_services_tests/rabbitmq/receiver.py ```

Publisher will send number every second, and consumer will print them.

## PostgreSQL

#### Test it

Requires psycopg2

``` $ python3 /external_services_tests/database/main.py ```