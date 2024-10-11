from backend.app.db.db_actions import get_data
from dotenv import load_dotenv
import os


load_dotenv()
MONGO_DB_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")


def get_recent_players(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='league'):
    """
    Retrieve recent player entries from the specified MongoDB collection for specific tiers.

    This function queries the MongoDB collection for player data, filters for entries
    belonging to the tiers 'challenger', 'grandmaster', and 'master', and returns a
    list of entries sorted by leaguePoints in descending order.

    Parameters:
    ----------
    db_uri : str
        The MongoDB connection URI.
    db_name : str
        The name of the MongoDB database to use.
    collection_name : str, optional
        The name of the MongoDB collection to query (default is 'league').

    Returns:
    -------
    list
        A list of dictionaries, each containing the tier and corresponding player entry.
        Each dictionary has the format:
        {
            'tier': <tier_value>,
            ...  # Other fields from the entry
        }

    Example:
    --------
    >>> players = get_recent_players()
    >>> print(players)
    [{'tier': 'challenger', 'entry': {...}}, {'tier': 'grandmaster', 'entry': {...}}, ...]
    """
    # Define the aggregation pipeline
    pipeline = [
        {
            '$match': {
                'tier': {'$in': ['CHALLENGER', 'GRANDMASTER', 'MASTER']}  # Filter for specific tiers
            }
        },
        {
            '$sort': {
                'added_at': -1  # Sort by added_date in descending order
            }
        },
        {
            '$group': {
                '_id': '$tier',  # Group by tier
                'entries': {'$first': '$entries'},  # Get the entries list from the most recent record
            }
        },
        {
            '$unwind': '$entries',
        },
        {
            '$project': {
                '_id': 0,  # Exclude the _id field from the output
                'tier': '$_id',  # Rename _id to tier
                'entry': '$entries',  # Include the entries field
            }
        }
    ]

    # Use the modified get_data function with the pipeline
    data = get_data(db_uri, db_name, collection_name, pipeline=pipeline)

    # Extract the entry objects from the results and add the tier at the front
    results = [
        {'tier': result['tier'], **result['entry']}  # Place tier first, then entry fields
        for result in data if 'entry' in result
    ]

    results.sort(key=lambda x: x.get('leaguePoints', 0), reverse=True)

    return results