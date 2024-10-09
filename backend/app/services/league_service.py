import httpx
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
import logging

from backend.app.transformers.league_to_accounts import transform_league_to_accounts
from backend.app.db.crud import create_accounts
# from backend.app.db.database import get_db
from backend.app.db.database import SessionLocal, init_db, list_tables

load_dotenv()

API_KEY = os.getenv("DEFAULT_RIOT_API_KEY")

# Configure logging
# logging.basicConfig(filename="league_data.log", level=logging.INFO, format="%(asctime)s - %(message)s")



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
    # available_tables = list_tables()
    # print("Available tables in the database:", available_tables)

    master_data = await fetch_master_leagues()
    grandmaster_data = await fetch_grandmaster_leagues()
    challenger_data = await fetch_challenger_leagues()

    # logging.info("After fetching master accounts from riot API:")
    # logging.info(master_data)

    # Transform data
    master_accounts = transform_league_to_accounts(master_data)
    grandmaster_accounts = transform_league_to_accounts(grandmaster_data)
    challenger_accounts = transform_league_to_accounts(challenger_data)

    # Save transformed data to the log file instead of the database
    # logging.info(f"Master accounts: {master_accounts}")
    # logging.info(f"Grandmaster accounts: {grandmaster_accounts}")
    # logging.info(f"Challenger accounts: {challenger_accounts}")

    # Save data to the database
    # logging.info("Preparing to insert master accounts:")
    # for account in master_accounts:
    #     logging.info(account)
    create_accounts(db=db, accounts=master_accounts)
    create_accounts(db=db, accounts=grandmaster_accounts)
    create_accounts(db=db, accounts=challenger_accounts)


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