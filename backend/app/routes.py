from fastapi import APIRouter
from backend.app.db.db_queries import query_player_stats_all, query_player_stats_by_id, compile_match_detail_from_puuid
import asyncio
import logging


# Configure logging
logging.basicConfig(
    filename="routes.log",  # Log file name
    level=logging.INFO,  # Logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format for timestamps
)

router = APIRouter()

@router.get("/api/player-stats")
async def get_player_stats_all_db():
    data = await query_player_stats_all()  # Fetch data from MongoDB
    return data

@router.get("/api/player-stats/{player_puuid}")
async def get_player_stats_db(player_puuid: str):
    data = await query_player_stats_by_id(player_puuid=player_puuid)  # Fetch data from MongoDB
    return data

@router.get("/api/player-match-history{player_puuid}")
async def get_player_match_history_db(player_puuid: str):
    logging.info(f"START ROUTE: /api/player-match-history{player_puuid}")
    data = await compile_match_detail_from_puuid(player_puuid=player_puuid)
    logging.info(f"returned data sample: {data[0:1]}")
    logging.info(f"returned data length: {len(data)}")
    logging.info(f"END ROUTE: /api/player-match-history{player_puuid}")
    return data



# Running the async function in an event loop
if __name__ == "__main__":
    sample_puuid = "RzdoQhmL8pdy8Oj8MweL584sMtP6pdn5TwcXpeq-9OnGeOmUrFaWc8NECbYF_kG4C0aQg-PjSxCuyQ"
    # results = asyncio.run(get_player_stats_all_db())
    # results = asyncio.run(get_player_stats_db(player_puuid=sample_puuid))
    results = asyncio.run(get_player_match_history_db(player_puuid=sample_puuid))
