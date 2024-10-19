from fastapi import APIRouter
from backend.app.db.db_queries import query_recent_players, query_player_puuids, query_match_ids, query_processed_match_ids, query_match_detail_ids, query_player_stats_match_details, query_player_summarized_stats
import asyncio

router = APIRouter()

@router.get("/api/your-data")
async def fetch_match_ids_db():
    data = await query_match_ids()  # Fetch data from MongoDB
    return data

# Running the async function in an event loop
if __name__ == "__main__":
    results = asyncio.run(fetch_match_ids_db())
    sample = results[0:10]
    print(f"sample, {sample}")
    print(len(results))
