from datetime import datetime

from pydantic.v1 import ValidationError

from backend.app.api.fetch_data import fetch_apex_leagues
from backend.app.db.db_actions import insert_data
from backend.app.db.db_queries import get_recent_players
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


if __name__ == "__main__":
    import asyncio
    # asyncio.run(update_league_data())
    asyncio.run(query_recent_players())