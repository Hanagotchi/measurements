# Measurements Microservice

## Documentation

### Environment Variables:

Configure the service:
* **LOGGING_LEVEL** (Default: "INFO"): Controls the level of logging output.
* **PORT** (Default: 8080): The port on which the service listens for requests.

Configure the connection to your PostgreSQL database:
* **POSTGRES_USER** 
* **POSTGRES_PASSWORD**
* **POSTGRES_DB**
* **POSTGRES_HOST**
* **POSTGRES_PORT** 
* **POSTGRES_SCHEMA**
* **DATABASE_URL**  

Configure the URLs of the other services:
* **PLANT_SERVICE_URL**
* **MEASUREMENTS_SERVICE_URL**
* **USERS_SERVICE_URL**

Configure the connection to your RabbitMQ server:
* **MQTT_HOST**
* **MQTT_PORT**
* **MQTT_USERNAME**
* **MQTT_PASSWORD**
* **MQTT_TOPIC**

Configure the connection to your Firebase server:
* **FIREBASE_CREDENTIALS** 

Configure the restrictions for sending notifications.
* **NOTIFICATION_RESTRICTIONS** 

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


## Run tests

To execute service unit tests, run:

``` $ python3 -m venv venv ```

``` $ source venv/bin/activate ```

``` $ pip install -r requirements.txt ```

``` $ cd app ```

``` $ python3 -m pytest ```