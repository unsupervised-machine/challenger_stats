import os
import httpx
from dotenv import load_dotenv


# ===============================
# Environment Variables Section
# ===============================

load_dotenv()
API_KEY = os.getenv("DEFAULT_RIOT_API_KEY")


# ===============================
# Leagues and Accounts
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


async def fetch_apex_leagues(apex_rank=None, queue="RANKED_SOLO_5x5", region="na1", api_key=API_KEY):
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


async def fetch_account_ids(region="na1", summoner_id=None, api_key=API_KEY):
    if not summoner_id:
        raise ValueError("Summoner ID cannot be blank.")

    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}?api_key={api_key}"
    # logging.info(f"Fetching account IDs for summoner ID: {summoner_id}")  # Log info

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        # logging.info(f"Successfully fetched account IDs for summoner ID: {summoner_id}")  # Log success
        return response.json()


# ===============================
# Matches
# ===============================


async def fetch_matches(region="americas", puuid=None, queue="420", start="0", count="100", api_key=API_KEY):
    if not puuid:
        raise ValueError("Puuid cannot be blank.")

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue={queue}&start={start}&count={count}&api_key={api_key}"
    # logging.info(f"Fetching {count} matches for PUUID: {puuid}, Queue: {queue}, Start: {start}, Count: {count}")  # Log info

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        # logging.info(f"Successfully fetched {count} matches for PUUID: {puuid}")  # Log success
        return response.json()


async def fetch_matches_all(region="americas", puuid=None, queue="420", count="100", api_key=API_KEY):
    if not puuid:
        raise ValueError("Puuid cannot be blank.")

    # logging.info(f"Fetching all matches for PUUID: {puuid}")

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

    # logging.info(f"Successfully fetched all matches for PUUID: {puuid}")
    return matches_all_list


async def fetch_match_details(region="americas", match_id=None, api_key=API_KEY):
    if not match_id:
        raise ValueError("Match ID cannot be blank.")

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    # logging.info(f"Fetching match details for match ID: {match_id}")
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        # logging.info(f"Successfully fetched match details for match ID: {match_id}")
        return response.json()


async def fetch_match_details_all(region="americas", match_id_list=None, api_key=API_KEY):
    if not match_id_list:
        raise ValueError("Match ID list cannot be blank.")

    # logging.info(f"Fetching match details for these match ids: {match_id_list}")

    match_details_all_list = []
    for match_id in match_id_list:
        match_details = await fetch_match_details(region=region, match_id=match_id, api_key=API_KEY)
        match_details_all_list.append(match_details)
        await asyncio.sleep(3)

    # logging.info(f"Successfully fetched match details for these match ids: {match_id_list}")
    return match_details_all_list
