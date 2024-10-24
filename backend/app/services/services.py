import time
from datetime import datetime, timedelta

from pydantic.v1 import ValidationError

from backend.app.api.fetch_data import fetch_apex_leagues, fetch_account_ids, fetch_matches_all, fetch_match_details_all, fetch_game_name_tagline, fetch_item_icons_ids
from backend.app.db.db_actions import insert_data, clear_and_insert_data, clear_collection_data, remove_records
from backend.app.db.db_queries import query_ladder_players, query_puuids, query_match_ids, query_processed_match_ids, query_match_detail_ids, compile_player_match_history, compile_player_summarized_stats, query_player_ids, compile_ladder
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
    logging.info(f"START SERVICE: update_league_data")
    # Fetch Data
    logging.info(f"Fetching data start: master league from NA")
    ladder_data = await fetch_apex_leagues()
    logging.info(f"Fetching data end: success \n Data length: {len(ladder_data)}")

    # Validate Data
    logging.info(f"Validating data start: \n need to implement validation...")
    # need to implement this with pydantic...
    validation_check = True
    logging.info(f"Validating data end: \n success")

    # Insert Data
    if validation_check:
        logging.info(f"Inserting data start: database {MONGO_DB_NAME}, collection league")
        insert_id = await clear_and_insert_data(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='league', data=ladder_data)
        logging.info(f"Inserting data end: success \n insert_id: {insert_id}")

    logging.info(f"END SERVICE: update_league_data")


async def update_player_ids_data():
    logging.info(f"START SERVICE: update_player_ids_data")
    # Fetch players from ladder (only id is summonerId)
    logging.info(f"Fetching data start: \n get recent_player data from db query")
    new_player_ids = await query_ladder_players()
    logging.info(f"Fetching data end: success \n Data: {new_player_ids[0:10]}")

    # Fetch players ids already stored in the database (also contains summonerId)
    logging.info(f"Fetching data start: \n get recent_player data from db query")
    stored_player_ids = await query_player_ids()
    logging.info(f"Fetching data end: success \n Data sample: {stored_player_ids[0:10]}")

    # Transform Data
    # Create sets of summonerIds from both lists
    new_player_ids_set = {d['summonerId'] for d in new_player_ids}
    stored_ids_set = {d['summonerId'] for d in stored_player_ids}
    # Find summonerIds unique to new_players_ids
    ids_to_fetch_and_store = new_player_ids_set - stored_ids_set

    # Fetch other ids (including puuid) along with game name and tagline
    ids_to_store = []
    for summoner_id in ids_to_fetch_and_store:
        account_ids = await fetch_account_ids(summoner_id=summoner_id)
        puuid = account_ids['puuid']
        name_and_tag_line = await fetch_game_name_tagline(puuid=puuid)
        combined_dict = {**account_ids, **name_and_tag_line}
        ids_to_store.append(combined_dict)


    # Validate Data
    logging.info(f"Validating data start: \n need to implement validation...")
    # need to implement this with pydantic...
    validation_check = True
    logging.info(f"Validating data end: \n success")

    # Insert Data
    logging.info(f"Inserting data start: \n database: {MONGO_DB_NAME}, collection: player_ids")
    logging.info(f"Sample of data trying to insert: {ids_to_store[0:10]}")
    if validation_check:
        insert_id = await insert_data(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='player_ids', data=ids_to_store)
        logging.info(f"Inserting data end: success \n insert_id length: {len(insert_id)}")

    logging.info(f"END SERVICE: update_player_ids_data")


async def update_match_ids():
    logging.info(f"START SERVICE: update_match_ids_data")

    # Start the timer
    start_time = time.time()

    # ~ 1 HOUR RUN TIME, with sleep time of 3 sec

    # Fetches
    # (1) Get puuids data from database
    # (2) Fetch match Ids from api using puuids
    logging.info(f"Fetching data start: \n get player puuid data from db query")
    puuid_data = await query_puuids()
    logging.info(f"Fetching data end: success \n Data length: {len(puuid_data)}")

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
        insert_id = await clear_and_insert_data(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='match_id',
                                          data=documents)
        logging.info(f"Inserting data end: success \n insert_id: {insert_id}")


    logging.info(f"END SERVICE: update_match_ids_data")
    # End the timer
    end_time = time.time()
    total_time = end_time - start_time
    logging.info(f"Total time taken: {total_time:.2f} seconds")


# 10/14/2024 Execution time: update_match_detail
    # From scratch to fully update database is currently expected to take ~ 15 hours or 5 hours per 10k records
    # starting from scratch will take longer as the season gets longer
    # if the table are already populated this should take a matter of minutes
async def update_match_detail():
    logging.info(f"START SERVICE: update_match_detail")
    # Capture the start time
    start_time = time.time()

    # Fetch 1
    logging.info(f"Fetching data start: \n Get match_id data from db query")
    match_id_data = await query_match_ids()
    logging.info(f"Fetching data end: success \n length: {len(match_id_data)}")

    logging.info(f"Fetching data start: \n Get processed_match_id data from db query")
    processed_match_id_data = await query_processed_match_ids()
    logging.info(f"Fetching data end: success \n length: {len(processed_match_id_data)}")

    # Transform 2
    logging.info(f"Transforming data start: \n Filter to find matches that need to be processed")
    match_ids_to_process = [match_id for match_id in match_id_data if match_id not in processed_match_id_data]
    logging.info(f"Transforming data end: success \n length: {len(match_ids_to_process)}")

    logging.info(f"Transforming data start: Truncate match_ids_to_process to 950 (to limit execution time)")
    match_ids_to_process = match_ids_to_process[0:10000]
    logging.info(f"Transforming data end: success \n length: {len(match_ids_to_process)}")

    # Fetch 2
    logging.info(f"Fetching data start: \n get match_details from api calls")
    match_details_list = []
    try:
        match_details_list = await fetch_match_details_all(match_id_list=match_ids_to_process)
    except Exception as e:
        logging.error(f"An error occurred while fetching match details: {e}", exc_info=True)

    logging.info(f"Fetching data end: success \n length: {len(match_details_list)}")

    # Transform 2
    logging.info(f"Transforming data start: marking processed matches true for database records")
    match_ids_to_process_list = [{"match_id": match_id, "processed_with_api_call": True} for match_id in match_ids_to_process]
    logging.info(f"Transforming data end: success , \n length: {len(match_ids_to_process_list)}")

    # Validation
    # validate data before insertion
    logging.info(f"Validating data start: \n need to implement validation...")
    # need to implement this with pydantic...
    validation_check = True
    logging.info(f"Validating data end: \n success")

    # Insertion 1
    logging.info(f"Inserting data start: \n database: {MONGO_DB_NAME}, collection: match_detail")
    if validation_check:
        insert_id_list = await insert_data(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='match_detail',
                                          data=match_details_list)
        logging.info(f"Inserting data end: success \n insert_id_list length: {len(insert_id_list)}")

    # Insertion 2
    # ONLY PREFORM THIS IF DATA HAS ACTUALLY BEEN INSERTED (VALIDATE THIS WITH QUERY?)
    logging.info(f"Inserting data start: \n database: {MONGO_DB_NAME}, collection: processed_match_id")
    if validation_check:
        insert_id_list = await insert_data(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='processed_match_id',
                                          data=match_ids_to_process_list)
        logging.info(f"Inserting data end: success \n insert_id_list length: {len(insert_id_list)}")

    # Capture the end time
    end_time = time.time()

    # Calculate the time difference
    time_difference = end_time - start_time

    # Format time differnce as hours minutes seconds
    formatted_duration = str(timedelta(seconds=time_difference))

    logging.info(f"END SERVICE: update_match_detail | Duration: {time_difference:.2f} seconds")


async def update_player_match_history():
    logging.info(f"START SERVICE: update_player_match_history")

    # Fetch list of all players from db query
    logging.info(f"Fetching data start: \n Get puuids data from db query")
    puuids_list = await query_puuids()
    logging.info(f"puuids_list sample: {puuids_list[0:10]}")

    logging.info(f"Fetching data end: success \n length: {len(puuids_list)}")

    logging.info(f"Transform data start: \n Generate player_match_history data from db query")
    players_match_history_list = []

    # Transform Generate player matches stats from database query
    for puuid in puuids_list:
        player_match_history = await compile_player_match_history(player_puuid=puuid)
        players_match_history_list.extend(player_match_history)
    logging.info(f"Transform data end: success \n length: {len(players_match_history_list)}")

    # Validation
    logging.info(f"Validating data start: \n need to implement validation...")
    validation_check = True
    logging.info(f"Validating data end: \n success")

    # Insert records into player_matches_stats
    logging.info(f"Data trying to insert: {players_match_history_list[0:10]}")

    logging.info(f"Inserting data start: \n database: {MONGO_DB_NAME}, collection: player_matches_stats")
    if validation_check:
        insert_id_list = await insert_data(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='player_match_history',
                                          data=players_match_history_list)
        logging.info(f"Inserting data end: success \n insert_id_list length: {len(insert_id_list)}")

    logging.info(f"END SERVICE: update_player_matches_stats")


async def update_player_summarized_stats():
    logging.info(f"START SERVICE: update_player_summarized_stats")

    # Fetch list of all players from db
    logging.info(f"Fetching data start: \n Get puuids data from db query")
    puuids_list = await query_puuids()
    logging.info(f"puuids_list sample: {puuids_list[0:10]}")
    logging.info(f"Fetching data end: success \n length: {len(puuids_list)}")

    # Transform generate player matches stats from database
    logging.info(f"Transform data start: \n Generate player_summarized_stats data from db query")
    player_summarized_stats_list = []
    for puuid in puuids_list:
        player_summarized_stats = await compile_player_summarized_stats(player_puuid=puuid)
        player_summarized_stats_list.extend(player_summarized_stats)
    logging.info(f"Transform data end: success \n length: {len(player_summarized_stats_list)}")

    # Validation
    logging.info(f"Validating data start: \n need to implement validation...")
    validation_check = True
    logging.info(f"Validating data end: \n success")

    # Insert records into player_matches_stats
    logging.info(f"Inserting data start: \n database: {MONGO_DB_NAME}, collection: player_summarized_stats")
    logging.info(f"Data trying to insert sample: {player_summarized_stats_list[0:10]}")

    if validation_check:
        insert_id_list = await clear_and_insert_data(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME, collection_name='player_summarized_stats',
                                          data=player_summarized_stats_list)
        logging.info(f"Inserting data end: success \n insert_id_list length: {len(insert_id_list)}")

    logging.info(f"END SERVICE: update_player_summarized_stats")


async def update_item_icons():
    logging.info(f"START SERVICE: update_item_icons")
    await fetch_item_icons_ids()
    logging.info(f"END SERVICE: update_item_icons")



async def update_ladder_data():
    logging.info(f"START SERVICE: update_ladder_data")
    ladder_data = await compile_ladder()
    logging.info(f"ladder_data sample: {ladder_data[0:10]}")
    logging.info(f"ladder_data length: {len(ladder_data)}")

    insert_id_list = await clear_and_insert_data(db_uri=MONGO_DB_URI, db_name=MONGO_DB_NAME,
                                                 collection_name='ladder',
                                                 data=ladder_data)
    logging.info(f"Inserting data end: success \n insert_id_list length: {len(insert_id_list)}")
    logging.info(f"END SERVICE: update_ladder_data")



async def _dev_clean_unprocessed_matches():
    logging.info(f"START SERVICE: _dev_clean_unprocessed_matches")
    claim = await query_processed_match_ids()
    logging.info(f"Claimed to be processed length: {len(claim)}")

    actual = await query_match_detail_ids()
    logging.info(f"Actual processed length: {len(actual)}")

    not_accounted_match_id = list(set(claim) - set(actual))
    logging.info(f"Not accounted for not_accounted_match_id: {len(not_accounted_match_id)}")
    logging.info(f"Sample data for not_accounted_match_id: {not_accounted_match_id[0:10]}")

    logging.info(f"Begin removing bad records")

    # THIS REMOVE RECORDS CAREFUL!!!
    removed_records_count =  await remove_records(db_uri=MONGO_DB_URI,
                                           db_name=MONGO_DB_NAME,
                                           collection_name='processed_match_id',
                                           data=not_accounted_match_id,
                                           unique_id='match_id')

    logging.info(f"Removed bad records: {removed_records_count}")

    new_claim = await query_processed_match_ids()
    logging.info(f"New claimed to be processed length: {len(new_claim)}")

    new_actual = await query_match_detail_ids()
    logging.info(f"New actual processed length: {len(new_actual)}")


    logging.info(f"END SERVICE: _dev_clean_unprocessed_matches")


async def _dev_clear_collection_data(collection_name="sample"):
    logging.info(f"START SERVICE: _dev_clear_collection_data")

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

    logging.info(f"END SERVICE: _dev_clear_collection_data")








if __name__ == "__main__":
    import asyncio
    # STANDARD SERVICES
    # asyncio.run(update_league_data())
    # asyncio.run(update_player_ids_data())
    # asyncio.run(update_game_name_taglines())
    # asyncio.run(update_match_ids())
    asyncio.run(update_match_detail())
    # asyncio.run(update_player_match_history())
    # asyncio.run(update_player_summarized_stats())
    # asyncio.run(update_ladder_data())
    # asyncio.run(update_item_icons())

    # DEV SERVICES
    asyncio.run(_dev_clean_unprocessed_matches())
    # asyncio.run(_dev_clear_collection_data())

    # TEST SERVICES


