from fastapi import APIRouter
from backend.app.db.db_queries import get_recent_players, get_player_puuids, get_match_ids, get_processed_match_ids, get_match_detail_ids, get_player_stats_match_details, get_player_summarized_stats
import asyncio

router = APIRouter()

@router.get("/api/your-data")
async def fetch_match_ids_db():
    data = await get_match_ids()  # Fetch data from MongoDB
    return data

# Running the async function in an event loop
if __name__ == "__main__":
    results = asyncio.run(fetch_match_ids_db())
    sample = results[0:10]
    print(f"sample, {sample}")
    print(len(results))
