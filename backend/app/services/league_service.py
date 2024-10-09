import httpx
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
import logging

from backend.app.transformers.league_to_accounts import transform_league_to_accounts_current, transform_league_to_accounts_history
from backend.app.db.crud import create_accounts_current, insert_accounts_history
# from backend.app.db.database import get_db
from backend.app.db.database import SessionLocal, init_db, list_tables

load_dotenv()

API_KEY = os.getenv("DEFAULT_RIOT_API_KEY")

async def fetch_challenger_leagues(queue="RANKED_SOLO_5x5", region="na1", api_key=API_KEY):
    url = f"https://{region}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/{queue}?api_key={api_key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()


async def fetch_grandmaster_leagues(queue="RANKED_SOLO_5x5", region="na1", api_key=API_KEY):
    url = f"https://{region}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/{queue}?api_key={api_key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()


async def fetch_master_leagues(queue="RANKED_SOLO_5x5", region="na1", api_key=API_KEY):
    url = f"https://{region}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/{queue}?api_key={api_key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()


async def process_leagues():
    db = SessionLocal()
    init_db()

    master_data = await fetch_master_leagues()
    grandmaster_data = await fetch_grandmaster_leagues()
    challenger_data = await fetch_challenger_leagues()

    # Transform data
    master_accounts_current = transform_league_to_accounts_current(master_data)
    grandmaster_accounts_current = transform_league_to_accounts_current(grandmaster_data)
    challenger_accounts_current = transform_league_to_accounts_current(challenger_data)

    master_accounts_history = transform_league_to_accounts_history(master_data)
    grandmaster_accounts_history= transform_league_to_accounts_history(grandmaster_data)
    challenger_accounts_history = transform_league_to_accounts_history(challenger_data)

    # Save only current run accounts to the current table
    current_accounts = master_accounts_current + grandmaster_accounts_current + challenger_accounts_current  # Combine all accounts for the current run
    create_accounts_current(db=db, accounts=current_accounts)
    print(f"length of current accounts: {len(current_accounts)}")

    # Insert records into historic table
    historic_accounts = master_accounts_history + grandmaster_accounts_history + challenger_accounts_history
    print(f"length of historic accounts: {len(historic_accounts)}")
    insert_accounts_history(db=db, accounts=historic_accounts)


async def test_fetches():
    print("Fetching Challenger Leagues...")
    challenger_leagues = await fetch_challenger_leagues()
    print("Challenger Leagues:", challenger_leagues)

    print("\nFetching Grandmaster Leagues...")
    grandmaster_leagues = await fetch_grandmaster_leagues()
    print("Grandmaster Leagues:", grandmaster_leagues)

    print("\nFetching Master Leagues...")
    master_leagues = await fetch_master_leagues()
    print("Master Leagues:", master_leagues)


async def test_inserts():
    print("Adding leagues to sqlite database")
    await process_leagues()
    print("Check database for inserts")



# Run the test
# python app/services/league_service.py
if __name__ == "__main__":
    import asyncio
    # asyncio.run(test_fetches())
    asyncio.run(test_inserts())