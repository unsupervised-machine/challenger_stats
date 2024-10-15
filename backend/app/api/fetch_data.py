import os
import httpx
from dotenv import load_dotenv
import asyncio


# ===============================
# Environment Variables Section
# ===============================

load_dotenv()
API_KEY = os.getenv("DEFAULT_RIOT_API_KEY")
SEASON_START_TIME_UNIX = os.getenv("SEASON_START_TIME_UNIX")
RATE_LIMIT = int(os.getenv("RATE_LIMIT"))


# ===============================
# Leagues and Accounts
# ===============================


async def fetch_challenger_leagues(queue="RANKED_SOLO_5x5", region="na1", api_key=API_KEY):
    # API LIMITS:
        # 30 requests every 10 seconds
        # 500 requests every 10 minutes

    url = f"https://{region}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/{queue}?api_key={api_key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()


async def fetch_grandmaster_leagues(queue="RANKED_SOLO_5x5", region="na1", api_key=API_KEY):
    # API LIMITS:
        # 30 requests every 10 seconds
        # 500 requests every 10 minutes

    url = f"https://{region}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/{queue}?api_key={api_key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()


async def fetch_master_leagues(queue="RANKED_SOLO_5x5", region="na1", api_key=API_KEY):
    # API LIMITS:
        # 30 requests every 10 seconds
        # 500 requests every 10 minutes

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
    # API LIMITS:
        #  1600 requests every 1 minutes

    if not summoner_id:
        raise ValueError("Summoner ID cannot be blank.")

    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}?api_key={api_key}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


# ===============================
# Matches
# ===============================
# Only watch fectch matches from recent seasons
# Season 14 Split 3 Start Date:
    # Date: Wednesday, September 25, 2024
    # Unix Seconds: 1727290800



async def fetch_matches(region="americas", puuid=None, start_time=SEASON_START_TIME_UNIX, queue="420", start="0", count="100", api_key=API_KEY):
    """
    get a set of match ids

    API LIMIT:
        2000 requests every 10 seconds
        12000 requests every 60 seconds

    :param start_time:
    :param region:
    :param puuid:
    :param queue: { ranked_solo_5x5: "420", }
    :param start: index where to start getting matches from
    :param count: how many matches to get starting from the start index
    :param api_key:
    :return:
    """

    if not puuid:
        raise ValueError("Puuid cannot be blank.")

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={start_time}&queue={queue}&start={start}&count={count}&api_key={api_key}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


async def fetch_matches_all(region="americas", puuid=None, start_time=SEASON_START_TIME_UNIX, queue="420", count="100", api_key=API_KEY):
    """
    get all the match_ids for a given puuid (capped at 1000 match_ids)
    :param start_time:
    :param region:
    :param puuid:
    :param queue:
    :param count:
    :param api_key:
    :return:
    """

    if not puuid:
        raise ValueError("Puuid cannot be blank.")


    matches_all_list = []

    start_int = 0
    start_str = str(start_int)

    while start_int < 1000: # max get 1000 games from a player
        # list of match ids
        matches = await fetch_matches(region=region, puuid=puuid, start_time=start_time, queue=queue, start=start_str, count=count, api_key=API_KEY)
        # stop early if no matches are in list
        if not matches:
            break

        matches_all_list.extend(matches)
        start_int += int(count)
        start_str = str(start_int)

        if len(matches_all_list) >= 1000:
            break

        await asyncio.sleep(RATE_LIMIT)

    return matches_all_list


async def fetch_match_details(region="americas", match_id=None, api_key=API_KEY):
    if not match_id:
        raise ValueError("Match ID cannot be blank.")

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


async def fetch_match_details_all(region="americas", match_id_list=None, api_key=API_KEY):
    if not match_id_list:
        raise ValueError("Match ID list cannot be blank.")


    match_details_all_list = []
    for match_id in match_id_list:
        match_details = await fetch_match_details(region=region, match_id=match_id, api_key=API_KEY)
        match_details_all_list.append(match_details)
        await asyncio.sleep(RATE_LIMIT)

    return match_details_all_list