import json
import logging
from database.models.device_plant import DevicePlant
from database.database import SQLAlchemyClient
from ..common.middleware import Middleware


class Consumer:
    def __init__(self, queue_name):
        self.__queue_name = queue_name
        self.__middleware = Middleware()
        self.__sqlAlchemyClient = SQLAlchemyClient()

    def run(self):
        self.__middleware.create_queue(self.__queue_name)
        self.__middleware.listen_on(self.__queue_name, self.__callback)

    def __callback(self, body):
        body = json.loads(body)
        print(body)
        dp = DevicePlant(id_device=body["id_device"],
                         id_plant=body["id_plant"],
                         plant_type=body["plant_type"],
                         id_user=body["id_user"])
        self.__sqlAlchemyClient.add_new(dp)
        logging.info("action: registro agregado a la base de datos|"
                     f"device_plant: {dp}")
