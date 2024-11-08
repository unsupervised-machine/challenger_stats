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


def clear_and_insert_data(db_uri, db_name, collection_name, data):
    db = get_db(db_uri, db_name)
    collection = db[collection_name]

    # Clear previous entries
    collection.delete_many({})

    # Insert new data
    if isinstance(data, list):
        result = collection.insert_many(data)
        return result.inserted_ids
    else:
        result = collection.insert_one(data)
        return result.inserted_id


def get_data(db_uri, db_name, collection_name, filter=None, sort_field=None, limit=None, projection=None, pipeline=None):
    db = get_db(db_uri, db_name)
    collection = db[collection_name]

    # If a pipeline is provided, use it for aggregation
    if pipeline:
        cursor = collection.aggregate(pipeline)
    else:
        # Apply the filter, sort, and limit if specified
        cursor = collection.find(filter, projection)
        if sort_field:
            cursor = cursor.sort(*sort_field)
        if limit:
            cursor = cursor.limit(limit)

    return list(cursor)


def clear_collection_data(db_uri, db_name, collection_name):
    """
    Clear all entries in a specified collection.

    :param db_uri: URI for the MongoDB database connection
    :param db_name: Name of the database
    :param collection_name: Name of the collection to clear
    :return: Result of the delete operation
    """
    db = get_db(db_uri, db_name)
    collection = db[collection_name]

    # Clear all entries in the collection
    result = collection.delete_many({})
    return result.deleted_count  # Returns the number of documents deleted


def remove_records(db_uri, db_name, collection_name, data, unique_id):
    db = get_db(db_uri, db_name)
    collection = db[collection_name]

    result = collection.delete_many({unique_id: {'$in': data}})
    return result.deleted_count
