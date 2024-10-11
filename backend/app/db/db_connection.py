from pymongo import MongoClient


class MongoDBConnection:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def close(self):
        self.client.close()