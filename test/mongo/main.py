
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

uri = "mongodb+srv://afirmapaz:<password>@testing.3fmylwg.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    db = client["dev"]

    result = db["device_plant"].insert_many([
        {"x": 1, "tags": ["dog", "cat"]},
        {"x": 2, "tags": ["cat"]},
        {"x": 2, "tags": ["mouse", "cat", "dog"]},
        {"x": 3, "tags": []},
    ])

    print(result)
except Exception as e:
    print(e)