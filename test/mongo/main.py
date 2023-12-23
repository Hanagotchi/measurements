
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

uri = "mongodb+srv://afirmapaz:<password>@testing.3fmylwg.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'))


try:
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")


    db = client[os.getenv("MONGO_DB")]

    # Insert new data
    result = db["device_plant"].insert_many([
        {"x": 1, "tags": ["dog", "cat"]},
        {"x": 2, "tags": ["cat"]},
        {"x": 2, "tags": ["mouse", "cat", "dog"]},
        {"x": 3, "tags": []},
    ])
    print(result)

    # Find those which x == 2
    result = list(db["device_plant"].find({"x": {"$eq": 2}}, limit=100))
    print(result)

    # Time to check!
    input("Check Mongo Atlas if the commited changes are reflected! Type anything when you're ready, and those changes will be deleted: ")

    # Delete all documents in the collection
    result = db["device_plant"].delete_many({})
    print(result)


except Exception as e:
    print(e)