from fastapi import APIRouter
from backend.app.db.db_queries import query_player_stats_all, query_player_stats_by_id, query_ladder_component, query_puuid_match_history
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

@router.get("/api/test")
async def test_route():
    data = {"message": "Hello, this is a test route!"}
    return data

@router.get("/api/test2")
async def test_route_2():
    data = {"message": "Hello, this is a test route!"}
    return data

@router.get("/api/test/{testNum}")
async def test_route_3(testNum: int):
    data = {"message": f"Hello, {testNum} this is a test route!"}
    return data

@router.get("/api/player-stats")
async def get_player_stats_all_db():
    data = await query_player_stats_all()  # Fetch data from MongoDB
    return data

@router.get("/api/player-stats/{player_puuid}")
async def get_player_stats_db(player_puuid: str):
    data = await query_player_stats_by_id(player_puuid=player_puuid)  # Fetch data from MongoDB
    return data

@router.get("/api/player-match-history/{player_puuid}")
async def get_player_match_history_db(player_puuid: str):
    logging.info(f"START ROUTE: /api/player-match-history{player_puuid}")
    data = await query_puuid_match_history(player_puuid=player_puuid)
    logging.info(f"returned data sample: {data[0:2]}")
    logging.info(f"returned data length: {len(data)}")
    logging.info(f"END ROUTE: /api/player-match-history{player_puuid}")
    return data


@router.get("/api/ladder")
async def get_ladder_db():
    logging.info(f"START ROUTE: /api/ladder")
    data = await query_ladder_component()
    logging.info(f"returned data sample: {data[0:1]}")
    logging.info(f"returned data length: {len(data)}")
    logging.info(f"END ROUTE: /api/ladder")
    return data


# Running the async function in an event loop
if __name__ == "__main__":
    sample_puuid = "RzdoQhmL8pdy8Oj8MweL584sMtP6pdn5TwcXpeq-9OnGeOmUrFaWc8NECbYF_kG4C0aQg-PjSxCuyQ"
    results = asyncio.run(get_player_stats_all_db())
    # results = asyncio.run(get_player_match_history_db(player_puuid=sample_puuid))
    print(results[0:1])
