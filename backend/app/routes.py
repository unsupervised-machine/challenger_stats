from fastapi import APIRouter
from backend.app.db.db_queries import get_match_ids
import asyncio

router = APIRouter()

@router.get("/api/your-data")
async def fetch_match_ids_db():
    data = await get_match_ids()  # Fetch data from MongoDB
    return data

# Running the async function in an event loop
if __name__ == "__main__":
    results = asyncio.run(fetch_match_ids_db())
    print(len(results))
