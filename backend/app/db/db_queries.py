import datetime

from backend.app.db.db_actions import get_data
from dotenv import load_dotenv
from datetime import datetime, timedelta
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

# Helper functions used with match details
async def extract_match_stats_from_match_details(match_details):
    match_stats = {
        "matchId": match_details['metadata']['matchId'],
        "gameMode": match_details['info']['gameMode'],
        "matchDate": datetime.fromtimestamp(match_details['info']['gameEndTimestamp'] / 1000).isoformat(),
        "matchDuration": str(timedelta(seconds=match_details['info']['gameDuration']))
    }

    return match_stats


async def extract_player_stats_from_match_details(player_index, match_details):
    player_stats = {
        # NOT DISPLAYED
        "playerIndex": player_index,
        "puuid": match_details['info']['participants'][player_index]['puuid'],
        "teamPosition": match_details['info']['participants'][player_index]['teamPosition'],
        "win": match_details['info']['participants'][player_index]['win'],
        "championName": match_details['info']['participants'][player_index]['championName'],
        # DISPLAYED
        "summonerName": match_details['info']['participants'][player_index]['summonerName'],
        "championId": match_details['info']['participants'][player_index]['championId'],
        "summoner1Id": match_details['info']['participants'][player_index]['summoner1Id'],
        "summoner2Id": match_details['info']['participants'][player_index]['summoner2Id'],
        "item0": match_details['info']['participants'][player_index]['item0'],
        "item1": match_details['info']['participants'][player_index]['item1'],
        "item2": match_details['info']['participants'][player_index]['item2'],
        "item3": match_details['info']['participants'][player_index]['item3'],
        "item4": match_details['info']['participants'][player_index]['item4'],
        "item5": match_details['info']['participants'][player_index]['item5'],
        "item6": match_details['info']['participants'][player_index]['item6'],
        "kills": match_details['info']['participants'][player_index]['kills'],
        "deaths": match_details['info']['participants'][player_index]['deaths'],
        "assists": match_details['info']['participants'][player_index]['assists'],
        "totalMinionsKilled": match_details['info']['participants'][player_index]['totalMinionsKilled']
    }
    return player_stats

async def extract_team_stats_from_match_details(match_details):
    team_stats = {}
    for player_index in range(10):
        player_data = await extract_player_stats_from_match_details(player_index, match_details)
        team_stats[player_index] = player_data
    return team_stats



async def compile_player_match_history(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='match_detail',
                                       player_puuid=None):

    # list of tuples [(player_index, match_details)]
    match_id_index_record_list = await compile_match_detail_from_puuid(db_uri, db_name, collection_name, player_puuid=player_puuid)

    # List to store player stats
    player_stats_list = []

    for match_id, player_index, match_details in match_id_index_record_list:
        try:

            match_stats = await extract_match_stats_from_match_details(match_details)
            player_stats = await extract_player_stats_from_match_details(player_index, match_details)
            team_stats = await extract_team_stats_from_match_details(match_details)

            combined_dict = {**match_stats, **player_stats, **team_stats}


            # Append stats as a tuple
            player_stats_list.append(combined_dict)

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
                "average_cs": {"$avg": "$totalMinionsKilled"},
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


async def compile_ladder(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME):
    # fetch league from db
        # keys
            # summonerId (summonerId)
        # fields
            # leaguePoints
            # tier

    # fetch player_ids from db
        # keys
            # puuid (puuid)
            # id (summonerId)
        # fields
            # profileIconId
            # gameName
            # tagline

    # fetch player_summarized_stats from db
        # keys
            # id (puuid)
        # fields
            # match_count
            # win rate
            # average_kills
            # average_deaths
            # average_assists
    pipeline = [
        # The table this pipeline will be run on is the league collection...
        # First join: player_ids based on (summonerId)
        {
            '$lookup': {
                'from': 'player_ids',
                'localField': 'summonerId',
                'foreignField': 'id',
                'as': 'player_ids_data'
            }
        },
        # Unwind the array to work with individual elements
        {
            '$unwind': {
                'path': '$player_ids_data',
                'preserveNullAndEmptyArrays': True  # This allows documents with no match to still appear
            }
        },
        # Second join: player_ids with player_summarized_stats based on (puuid)
        {
            '$lookup': {
                'from': 'player_summarized_stats',  # The third collection to join
                'localField': 'player_ids_data.puuid',  # Field from collection2
                'foreignField': '_id',  # Field from collection3
                'as': 'player_summarized_stats_data'  # The output array where joined data will be stored
            }
        },
        {
            '$unwind': {
                'path': '$player_summarized_stats_data',
                'preserveNullAndEmptyArrays': True  # Preserve documents if no match is found
            }
        }
    ]

    # Run the aggregation on collection1
    results = await get_data(db_uri=db_uri, db_name=db_name, collection_name="league", pipeline=pipeline)
    return results


async def query_ladder_component(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='ladder'):
    projection = {
        "_id": 0,
        "tier":1,
        "leaguePoints": 1,
        "player_summarized_stats_data.average_win_rate": 1,
        "player_ids_data.profileIconId": 1,
        "player_ids_data.gameName": 1,
        "player_ids_data.tagLine": 1
    }

    # should be sorted when we query it
    results = await get_data(db_uri, db_name, collection_name, projection=projection)
    return results
