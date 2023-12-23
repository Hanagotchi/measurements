import os
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from .database import Database

class Mongo(Database):

    def __init__(self):
        load_dotenv()

        # Create a new client and connect to the server
        self.client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'))

        # Send a ping to confirm a successful connection
        self.client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

        self.db = self.client[os.getenv("MONGO_DB")]

    def shutdown(self):
        pass

    def insert_into_device_plant(self, id_device, id_plant, plant_type, id_user):
        return self.db["device_plant"].insert_one({
            "_id": id_device, 
            "id_plant": id_plant,
            "plant_type": plant_type,
            "id_user": id_user
        })

    def find_in_device_plant(self, id_device):
        return self.db["device_plant"].find_one({"_id": {"$eq": id_device}})
    
    def clean_device_plant(self):
        self.db["device_plant"].delete_many({})