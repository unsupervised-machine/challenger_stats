import os

from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()
# MONGO_DB_URI = os.getenv("MONGO_URI")
# MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# Helper
def get_db_client(db_uri):
    try:
        client = MongoClient(db_uri)
        return client
    except Exception as e:
        print(f"Failed to connect to MongoDB uri: {e}")
        return None

# Use this one
def get_db(db_uri, db_name):
    client = get_db_client(db_uri)
    if client:
        return client[db_name]
    else:
        raise Exception("Could not connect to MongoDB db_name")