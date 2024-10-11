# account_service.py

# ===============================
# Import Section
# ===============================

# Standard library imports (built-in modules)
import os
import logging

# Package imports (third-party libraries installed via pip)
import httpx
from dotenv import load_dotenv


# ===============================
# Environment Variables Section
# ===============================

load_dotenv()
API_KEY = os.getenv("DEFAULT_RIOT_API_KEY")


# ===============================
# Logging Setup
# ===============================
# Set up basic logging configuration
logging.basicConfig(
    filename="account_service.log",  # Log file name
    level=logging.INFO,  # Logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format for timestamps
)


# ===============================
# Function Definitions Section
# ===============================

async def fetch_account_ids(region="na1", summoner_id=None, api_key=API_KEY):
    if not summoner_id:
        raise ValueError("Summoner ID cannot be blank.")

    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}?api_key={api_key}"
    logging.info(f"Fetching account IDs for summoner ID: {summoner_id}")  # Log info

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        logging.info(f"Successfully fetched account IDs for summoner ID: {summoner_id}")  # Log success
        return response.json()


async def fetch_matches(region="americas", puuid=None, queue="420", start="0", count="100", api_key=API_KEY):
    if not puuid:
        raise ValueError("Puuid cannot be blank.")

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue={queue}&start={start}&count={count}&api_key={api_key}"
    logging.info(f"Fetching {count} matches for PUUID: {puuid}, Queue: {queue}, Start: {start}, Count: {count}")  # Log info

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        logging.info(f"Successfully fetched {count} matches for PUUID: {puuid}")  # Log success
        return response.json()


async def fetch_matches_all(region="americas", puuid=None, queue="420", count="100", api_key=API_KEY):
    if not puuid:
        raise ValueError("Puuid cannot be blank.")

    logging.info(f"Fetching all matches for PUUID: {puuid}")

    matches_all_list = []

    start_int = 0
    start_str = str(start_int)

    while start_int < 1000:
        # list of match ids
        matches = await fetch_matches(region=region, puuid=puuid, queue=queue, start=start_str, count=count, api_key=API_KEY)
        # stop early if no matches are in list
        if not matches:
            break

        matches_all_list.extend(matches)
        start_int += 100
        start_str = str(start_int)

        if len(matches_all_list) >= 1000:
            break

        await asyncio.sleep(3)

    logging.info(f"Successfully fetched all matches for PUUID: {puuid}")
    return matches_all_list


# noinspection DuplicatedCode
async def fetch_match_details(region="americas", match_id=None, api_key=API_KEY):
    if not match_id:
        raise ValueError("Match ID cannot be blank.")

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    logging.info(f"Fetching match details for match ID: {match_id}")
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        logging.info(f"Successfully fetched match details for match ID: {match_id}")
        return response.json()


async def fetch_match_details_all(region="americas", match_id_list=None, api_key=API_KEY):
    if not match_id_list:
        raise ValueError("Match ID list cannot be blank.")

    logging.info(f"Fetching match details for these match ids: {match_id_list}")

    match_details_all_list = []
    for match_id in match_id_list:
        match_details = await fetch_match_details(region=region, match_id=match_id, api_key=API_KEY)
        match_details_all_list.append(match_details)
        await asyncio.sleep(3)

    logging.info(f"Successfully fetched match details for these match ids: {match_id_list}")
    return match_details_all_list

# ===============================
# Script Tests
# ===============================
async def test_fetches():
    logging.info("Running Test: test_fetches")

    logging.info("Fetching account information from sample summoner id: AlHqCXpis9yPjHp2B0i3uY5Rq2NVo9lwX5178Gww6u6HzDo")
    account_ids = await fetch_account_ids(summoner_id="AlHqCXpis9yPjHp2B0i3uY5Rq2NVo9lwX5178Gww6u6HzDo")
    logging.info(f"Account Ids: {account_ids}")

    logging.info("Fetching match ids from sample puuid: 7Wys1Io3D-3pi0reuUUj7pc3IzyuBh39MLG-iuFP6fQD1j8x_u7Tz_NiNErNE8wkFAvbOM0zuUSbNQ")
    match_ids = await fetch_matches(puuid="7Wys1Io3D-3pi0reuUUj7pc3IzyuBh39MLG-iuFP6fQD1j8x_u7Tz_NiNErNE8wkFAvbOM0zuUSbNQ", start="10")
    logging.info(f"Match Ids: {match_ids}")
    logging.info(f"Match Ids length: {len(match_ids)}")

    logging.info("Fetching all match ids from sample puuid: 7Wys1Io3D-3pi0reuUUj7pc3IzyuBh39MLG-iuFP6fQD1j8x_u7Tz_NiNErNE8wkFAvbOM0zuUSbNQ")
    match_ids = await fetch_matches_all(puuid="7Wys1Io3D-3pi0reuUUj7pc3IzyuBh39MLG-iuFP6fQD1j8x_u7Tz_NiNErNE8wkFAvbOM0zuUSbNQ")
    logging.info(f"Match Ids: {match_ids}")
    logging.info(f"Match Ids length: {len(match_ids)}")

    logging.info("Fetching match details from sample match: NA1_5018289177")
    match_details = await fetch_match_details(region="americas", match_id="NA1_5018289177")
    logging.info(f"Match Details: {match_details}")

    logging.info("Fetching all match details from sample puuid: 7Wys1Io3D-3pi0reuUUj7pc3IzyuBh39MLG-iuFP6fQD1j8x_u7Tz_NiNErNE8wkFAvbOM0zuUSbNQ")
    match_details_all = await fetch_match_details_all(match_id_list=match_ids)
    logging.info(f"Match Details length: {len(match_details_all)}")

    logging.info("Finished Test: test_fetches")


# ===============================
# Main Function or Application Logic
# ===============================
if __name__ == "__main__":
    import asyncio
    asyncio.run(test_fetches())