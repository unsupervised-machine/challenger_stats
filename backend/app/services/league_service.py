# league_service.py

# ===============================
# Import Section
# ===============================

# Standard library imports (built-in modules)
import os
import logging

# Package imports (third-party libraries installed via pip)
import httpx
from dotenv import load_dotenv

# Local imports (modules or scripts within your project)
from backend.app.transformers.league_to_accounts import transform_league_to_accounts_current, transform_league_to_accounts_history
from backend.app.db.crud import create_accounts_current, insert_accounts_history
from backend.app.db.database import SessionLocal, init_db


# ===============================
# Environment Variables Section
# ===============================

load_dotenv()
API_KEY = os.getenv("DEFAULT_RIOT_API_KEY")


# ===============================
# Function Definitions Section
# ===============================

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


async def fetch_apex_leagues(apex_rank, queue="RANKED_SOLO_5x5", region="na1", api_key=API_KEY):
    """
    Fetches data from one of the apex leagues (Challenger, Grandmaster, or Master)
    based on the provided apex_rank parameter.

    :param apex_rank: The rank to fetch data for. Should be one of 'challenger', 'grandmaster', or 'master'.
    :param queue: The queue type (default is "RANKED_SOLO_5x5").
    :param region: The region to fetch data from (default is "na1").
    :param api_key: The API key to authenticate the request.
    :return: The JSON response of the requested league data.
    """
    if apex_rank == "challenger":
        return await fetch_challenger_leagues(queue=queue, region=region, api_key=api_key)
    elif apex_rank == "grandmaster":
        return await fetch_grandmaster_leagues(queue=queue, region=region, api_key=api_key)
    elif apex_rank == "master":
        return await fetch_master_leagues(queue=queue, region=region, api_key=api_key)
    else:
        raise ValueError(f"Invalid apex_rank '{apex_rank}'. Must be one of 'challenger', 'grandmaster', or 'master'.")



async def process_leagues():
    """
    Fetch, transform, and save data from multiple league tiers (Master, Grandmaster, Challenger)
    into both current and historical database tables.

    This function:
    1. Initializes the database session and fetches the latest data for Master, Grandmaster, and Challenger leagues asynchronously.
    2. Transforms the fetched league data into two formats:
        - A 'current' format containing the most recent accounts.
        - A 'history' format for the historical records of accounts.
    3. Combines the accounts data for all leagues and:
        - Saves the current run accounts into the 'current' accounts table.
        - Inserts the transformed historical data into the 'history' accounts table.
    4. Outputs the length of the current and historic accounts processed.
    :return:
    """
    db = SessionLocal()
    init_db()

    # master_data = await fetch_master_leagues()
    # grandmaster_data = await fetch_grandmaster_leagues()
    # challenger_data = await fetch_challenger_leagues()

    master_data = await fetch_apex_leagues(apex_rank="master")
    grandmaster_data = await fetch_apex_leagues(apex_rank="grandmaster")
    challenger_data = await fetch_apex_leagues(apex_rank="challenger")

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


# ===============================
# Script Tests
# ===============================

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


# ===============================
# Main Function or Application Logic
# ===============================

if __name__ == "__main__":
    import asyncio
    # asyncio.run(test_fetches())
    asyncio.run(test_inserts())