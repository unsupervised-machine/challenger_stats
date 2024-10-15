from datetime import datetime

from pydantic.v1 import ValidationError
from typing_extensions import assert_never

from backend.app.api.fetch_data import fetch_apex_leagues, fetch_account_ids, fetch_matches_all, fetch_match_details_all
from backend.app.db.db_actions import insert_data, clear_and_insert_data, clear_collection_data
from backend.app.db.db_queries import get_recent_players, get_player_puuids, get_match_ids, get_processed_match_ids
from backend.app.api.validation import League
from backend.app.api.transform_data import add_timestamps

from dotenv import load_dotenv
import os
import logging


load_dotenv()
MONGO_DB_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

logging.basicConfig(
    filename="services.log",  # Log file name
    level=logging.INFO,  # Logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format for timestamps
)

# =======================================
# BASIC SET UP FOR FUNCTIONS IN THIS FILE
# =======================================
# Fetch Data
# use api/fetch_data.py to preform api calls

# Transform Data
# When transforms are needed write them in api/transform_data.py as needed

# Validate Data
# Use pydantic to ensure data is in correct format before inserting, write them in api/validation.py as needed

# Insert Data
# use db/db_actions.py to preform database inserts
# =======================================


# Fetch Data
async def update_league_data():
    # Fetch Data
    logging.info(f"Fetching data start: master league from NA")
    data = await fetch_apex_leagues(apex_rank='master')
    logging.info(f"Fetching data end: success \n Data: {data}")

    # Transform Data
    logging.info(f"Transforming data start: \n Transformations applied: add_timestamps")
    data = add_timestamps(data=data, field='added_at')
    logging.info(f"Transforming data end: success \n Data: {data}")

    # Validate Data
    logging.info(f"Validating data start: pydantic model League")
    try:
        league_data  = League(**data)
        # league_data  = League(**data, added_at=datetime.now())
        validated_data = league_data.model_dump()
        logging.info(f"Validating data end: success \n Validated data: {validated_data}")
    except ValidationError as e:
        logging.info(f"Validation failed: {e}")
        return

    # Insert Data
    logging.info(f"Inserting data start: database {MONGO_DB_NAME}, collection league")
    insert_id = insert_data(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='league', data=validated_data)
    logging.info(f"Inserting data end: success \n insert_id: {insert_id}")


async def query_recent_players():
    # Fetch Data
    logging.info(f"Database query start: get_recent_players")
    data = get_recent_players()
    logging.info(f"Database query end: length is {len(data)} \n Data: {data}")

    # Transform Data
    # Since this is a query we only need to fetch the data...

    # Validate Data
    # Since this is a query we only need to fetch the data...

    # Insert Data
    # Since this is a query we only need to fetch the data...


async def update_player_ids_data():
    # Fetch Data
    logging.info(f"Fetching data start: \n get recent_player data from db query")
    apex_league_data = get_recent_players()
    logging.info(f"Fetching data end: success \n Data: {apex_league_data}")

    # Transform Data
    logging.info(f"Transforming data start: \n Transformations applied: fetch additional ids from api for each summonerId")
    summoner_ids = [item['summonerId'] for item in apex_league_data]


    player_ids = []
    for summoner_id in summoner_ids:
        account_data = await fetch_account_ids(summoner_id=summoner_id)  # Awaiting the async function
        player_ids.append({
            "summonerId": account_data["id"],
            "accountId": account_data["accountId"],
            "puuid": account_data["puuid"],
            "profileIconId": account_data["profileIconId"],
            "revisionDate": account_data["revisionDate"],
            "summonerLevel": account_data["summonerLevel"],
        })
        await asyncio.sleep(1.2)

    logging.info(f"Transforming data end: \n Data: {player_ids}")

    # Validate Data
    logging.info(f"Validating data start: \n need to implement validation...")
    # need to implement this with pydantic...
    validation_check = True
    logging.info(f"Validating data end: \n success")

    # Insert Data
    logging.info(f"Inserting data start: \n database: {MONGO_DB_NAME}, collection: player_ids")
    if validation_check:
        insert_id = clear_and_insert_data(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='player_ids', data=player_ids)
        logging.info(f"Inserting data end: success \n insert_id: {insert_id}")


async def update_match_ids_data():
    # ~ 1 HOUR RUN TIME, with sleep time of 3 sec

    # Fetches
    # (1) Get puuids data from database
    # (2) Fetch match Ids from api using puuids
    logging.info(f"Fetching data start: \n get player puuid data from db query")
    puuid_data = get_player_puuids()
    logging.info(f"Fetching data end: success \n Data: {puuid_data}")

    match_ids_set = set()  # use a set to avoid adding duplicate match_ids
    for puuid in puuid_data:
        match_ids = await fetch_matches_all(puuid=puuid)
        match_ids_set.update(match_ids)

    # Transforms
    # transform the match ids into proper format for database insert
    match_ids_list = list(match_ids_set)  # convert to a list so pymongo can insert it into db
    insert_timestamp = datetime.now()
    documents = [{"match_id": match_id, "inserted_at": insert_timestamp} for match_id in match_ids_list]


    # Validation
    # validate data before insertion
    logging.info(f"Validating data start: \n need to implement validation...")
    # need to implement this with pydantic...
    validation_check = True
    logging.info(f"Validating data end: \n success")

    # Insertion
    # clear table and insert data
    logging.info(f"Inserting data start: \n database: {MONGO_DB_NAME}, collection: match_id")
    if validation_check:
        insert_id = clear_and_insert_data(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='match_id',
                                          data=documents)
        logging.info(f"Inserting data end: success \n insert_id: {insert_id}")


async def update_processed_match_ids():
    logging.info(f"START: update_processed_match_ids")
    # Fetch
    logging.info(f"Fetching data start: \n get match_ids data from db query")
    match_id_data = get_match_ids()
    logging.info(f"Fetching data end: success \n Data: {match_id_data}, \n length: {len(match_id_data)}")

    logging.info(f"Fetching data start: \n get processed_match_id data from db query")
    processed_match_id_data = get_processed_match_ids()
    logging.info(f"Fetching data end: success \n Data: {processed_match_id_data}, \n length: {len(processed_match_id_data)}")

    # Transform
    logging.info(f"Transforming data start: \n Filter to find matches that need to be processed")
    match_ids_to_process = [match_id for match_id in match_id_data if match_id not in processed_match_id_data]
    logging.info(f"Transforming data end: success \n Data: {match_ids_to_process}, \n length: {len(match_ids_to_process)}")

    logging.info(f"Transforming data start: Truncate match_ids_to_process to 10 (to limit execution time)")
    match_ids_to_process = match_ids_to_process[0:10]
    logging.info(f"Transforming data end: success \n Data: {match_ids_to_process}, \n length: {len(match_ids_to_process)}")

    logging.info(f"Preforming api call on each of the matches...")
    match_details_list = await fetch_match_details_all(match_id_list=match_ids_to_process)
    logging.info(f"Finished api processing matches \n Data: {match_details_list} \n length: {len(match_details_list)}")

    logging.info(f"Preparing marking processed matches true for database records")
    match_ids_to_process_list = [{"match_id": match_id, "processed_with_api_call": True} for match_id in match_ids_to_process]
    logging.info(f"Finished preparing matches true for database records")

    # Validation
    # validate data before insertion
    logging.info(f"Validating data start: \n need to implement validation...")
    # need to implement this with pydantic...
    validation_check = True
    logging.info(f"Validating data end: \n success")

    # Insertion 1
    logging.info(f"Inserting data start: \n database: {MONGO_DB_NAME}, collection: match_detail")
    if validation_check:
        insert_id = insert_data(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='match_detail',
                                          data=match_details_list)
        logging.info(f"Inserting data end: success \n insert_id: {insert_id}")

    # Insertion 2
    # ONLY PREFORM THIS IF DATA HAS ACTUALLY BEEN INSERTED (VALIDATE THIS WITH QUERY?)
    logging.info(f"Inserting data start: \n database: {MONGO_DB_NAME}, collection: processed_match_id")
    if validation_check:
        insert_id = insert_data(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='processed_match_id',
                                          data=match_ids_to_process_list)
        logging.info(f"Inserting data end: success \n insert_id: {insert_id}")



    logging.info(f"END: update_processed_match_ids")


async def test_get_match_ids():
    logging.info(f"Fetching data start: \n get match_ids data from db query")
    puuid_data = get_match_ids()
    logging.info(f"Fetching data end: success \n Data: {puuid_data}")


async def test_get_processed_match_ids():
    logging.info(f"Fetching data start: \n get processed_match_ids data from db query")
    puuid_data = get_processed_match_ids()
    logging.info(f"Fetching data end: success \n Data: {puuid_data}")


async def _dev_clear_collection_data(collection_name="sample"):
    # Prompt the user for confirmation
    confirmation = input(
        f"Are you sure you want to clear all data from the '{collection_name}' collection? (yes/no): ").strip().lower()

    if confirmation == 'yes':
        deleted_count = clear_collection_data(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME,
                                              collection_name=collection_name)
        logging.info(f'Deleted {deleted_count} documents from the collection: {collection_name}.')
        print(f'Deleted {deleted_count} documents from the collection.')
    else:
        logging.info("Operation canceled by user. No data was deleted.")
        print("Operation canceled. No data was deleted.")


if __name__ == "__main__":
    import asyncio
    # asyncio.run(update_league_data())
    # asyncio.run(query_recent_players())
    # asyncio.run(update_player_ids_data())
    # asyncio.run(update_match_ids_data())
    # asyncio.run(update_processed_match_ids())
    asyncio.run(_dev_clear_collection_data())

    # asyncio.run(test_get_match_ids())
    # asyncio.run(test_get_processed_match_ids())

