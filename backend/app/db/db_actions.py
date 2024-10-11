from backend.app.db.db_connection import get_db


def insert_data(db_uri, db_name, collection_name, data):
    db = get_db(db_uri, db_name)
    collection = db[collection_name]

    if isinstance(data, list):
        result = collection.insert_many(data)
        return result.inserted_ids
    else:
        result = collection.insert_one(data)
        return result.inserted_id


