from fastapi import APIRouter
from backend.app.db.db_queries import query_player_stats_all, query_player_stats_by_id, compile_match_detail_from_puuid
import asyncio

router = APIRouter()

@router.get("/api/player-stats")
async def get_player_stats_all_db():
    data = await query_player_stats_all()  # Fetch data from MongoDB
    return data

@router.get("/api/player-stats/{puuid}")
async def get_player_stats_db(player_puuid: str):
    data = await query_player_stats_by_id(player_puuid=player_puuid)  # Fetch data from MongoDB
    return data

@router.get("/api/player-match-history{puuid}")
async def get_player_match_history_db(player_puuid: str):
    data = await compile_match_detail_from_puuid(player_puuid=player_puuid)



# Running the async function in an event loop
if __name__ == "__main__":
    results = asyncio.run(get_player_stats_all_db())
    # results = asyncio.run(get_player_stats_db(player_puuid="RzdoQhmL8pdy8Oj8MweL584sMtP6pdn5TwcXpeq-9OnGeOmUrFaWc8NECbYF_kG4C0aQg-PjSxCuyQ"))


    sample = results[0:10]
    print(f"sample, {sample}")
    print(len(results))
