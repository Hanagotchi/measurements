# Measurements Microservice

## Documentation

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


## PostgreSQL

#### Test it

``` $ python3 /external_services_tests/database/main.py ```