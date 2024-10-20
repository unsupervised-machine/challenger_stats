from backend.app.db.db_actions import get_data
from dotenv import load_dotenv
import os


load_dotenv()
MONGO_DB_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")


async def query_ladder_players(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='league'):
   ladder_data = await get_data(db_uri=db_uri, db_name=db_name, collection_name=collection_name)
   return ladder_data


async def query_player_ids(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='player_ids'):
    player_ids = await get_data(db_uri=db_uri, db_name=db_name, collection_name=collection_name)
    return player_ids

async def query_puuids(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='player_ids'):
    projection = {
        "_id": 0,
        "puuid": 1  # include summonerId in query return (exclude fields not set to 0)
    }
    data =  await get_data(db_uri, db_name, collection_name, projection=projection)
    results = [item['puuid'] for item in data]

    return results


async def query_match_ids(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='match_id'):
    """
    get all match ids stored in database
    :param db_uri:
    :param db_name:
    :param collection_name:
    :return:
    """
    projection = {
        "_id": 0,
        "match_id": 1,
    }
    data = await get_data(db_uri, db_name, collection_name, projection=projection)
    results = [item['match_id'] for item in data]
    return results


async def query_processed_match_ids(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='processed_match_id'):
    """
    get all match ids that have been processed through api call
    :param db_uri:
    :param db_name:
    :param collection_name:
    :return:
    """
    projection = {
        "_id": 0,
        "match_id": 1
    }
    filter = {
        "processed_with_api_call": True
    }

    data = await get_data(db_uri, db_name, collection_name, projection=projection, filter=filter)
    results = [item['match_id'] for item in data]
    return results

async def query_match_detail_ids(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='match_detail'):
    """
    this will mostly be used to validate the data is in match detail before updating processed_match_id
    :param db_uri:
    :param db_name:
    :param collection_name:
    :return:
    """
    projection = {
        "_id": 0,
        "metadata.matchId": 1
    }
    data = await get_data(db_uri, db_name, collection_name, projection=projection)
    results = [doc['metadata']['matchId'] for doc in data if 'metadata' in doc and 'matchId' in doc['metadata']]

    return results


async def compile_match_detail_from_puuid(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='match_detail',
                                          player_puuid=None):
    """
    return list of tuples of all match details which contain specified player, along with the participant index of the player in the match, and the matchId
    :param db_uri:
    :param db_name:
    :param collection_name:
    :param player_puuid:
    :return:
    """

    pipeline = [
        {
            "$match": {
                "metadata.participants": player_puuid
            }
        },
        {
            "$addFields": {
                "playerIndex": {
                    "$indexOfArray": ["$metadata.participants", player_puuid]
                }
            }
        },
        {
            "$sort": {
                "info.gameEndTimestamp": -1  # Sort by gameEndTimestamp in descending order
            }
        },
        {
            "$project": {
                "matchId": "$metadata.matchId",
                "playerIndex": "$playerIndex",
                "record": "$$ROOT"  # Keep the entire record if needed
            }
        }
    ]

    matching_records = await get_data(db_uri, db_name, collection_name, pipeline=pipeline)

    # Transform the result into the desired format
    player_record_tuples = [(record['matchId'], record['playerIndex'], record['record']) for record in matching_records]

    return player_record_tuples


async def compile_player_stats_match_details(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='match_detail',
                                             player_puuid=None):

    # list of tuples [(player_index, match_details)]
    match_id_index_record_list = await compile_match_detail_from_puuid(db_uri, db_name, collection_name, player_puuid=player_puuid)

    # List to store player stats
    player_stats_list = []

    for match_id, player_index, match_details in match_id_index_record_list:
        try:
            participant_data = match_details['info']['participants'][player_index]
            player_stats = {
                "match_id": match_id,
                "player_index": player_index,
                "puuid": participant_data['puuid'],
                "kills": participant_data['kills'],
                "deaths": participant_data['deaths'],
                "assists": participant_data['assists'],
                "champion_name": participant_data['championName'],
                "champion_id": participant_data['championId'],
                "team_position": participant_data['teamPosition'],
                "win": participant_data['win']
            }

            # Append stats as a tuple
            player_stats_list.append(player_stats)

        except (KeyError, IndexError) as e:
            print(f"Error extracting data for player index {player_index} in match {match_id}: {e}")

    return player_stats_list



async def compile_player_summarized_stats(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='player_matches_stats',
                                          player_puuid=None):
    pipeline = [
        {"$match": {"puuid": player_puuid}},
        {
            "$group": {
                "_id": "$puuid",
                "average_kills": {"$avg": "$kills"},
                "average_deaths": {"$avg": "$deaths"},
                "average_assists": {"$avg": "$assists"},
                "match_count": {"$sum": 1},
                "average_win_rate": {
                    "$avg": {
                        "$cond": {
                            "if": {"$eq": ["$win", True]},
                            "then": 1,
                            "else": 0
                        }
                    }
                }
            }
        }
    ]

    result = await get_data(db_uri, db_name, collection_name, pipeline=pipeline)

    return result


async def query_player_stats_all(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='player_summarized_stats'):
    results = await get_data(db_uri, db_name, collection_name)
    return results


async def query_player_stats_by_id(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='player_summarized_stats',
                             player_puuid=None):
    filter = {
        "_id": player_puuid
    }
    results = await get_data(db_uri, db_name, collection_name, filter=filter)
    return results


async def compile_ladder_data(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='ladder_data'):
    # fetch player_ids from db
        # keys
            # puuid (puuid)
            # id (summonerId)
        # fields
            # profile icon id
            # gameName
            # tagline

    # fetch league from db
        # keys
            # summonerId (summonerId)
        # fields
            # leaguePoints
            # tier

    # fetch player_summarized_stats from db
        # keys
            # id (puuid)
        # fields
            # match_count
            # win rate
            # average_kills
            # average_deaths
            # average_assists
