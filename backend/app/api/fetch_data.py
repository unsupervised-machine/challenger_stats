import os
import httpx
from dotenv import load_dotenv
import asyncio
import re
from pathlib import Path


# ===============================
# Environment Variables Section
# ===============================

load_dotenv()
API_KEY = os.getenv("DEFAULT_RIOT_API_KEY")
SEASON_START_TIME_UNIX = os.getenv("SEASON_START_TIME_UNIX")
RATE_LIMIT = float(os.getenv("RATE_LIMIT"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES"))
INITIAL_BACKOFF = float(os.getenv("INITIAL_BACKOFF"))


# ===============================
# Helper Functions
# ===============================
async def backoff_api_call(api_func, *args, **kwargs):
    """
    A generic function to apply exponential backoff on API calls.
    Retries on 429 (Too Many Requests) errors.

    :param api_func: the asynchronous function to call (e.g., fetch_matches)
    :param args: positional arguments to pass to the API function
    :param kwargs: keyword arguments to pass to the API function
    :return: the API response (JSON)
    """
    retries = 0
    backoff = INITIAL_BACKOFF

    while retries < MAX_RETRIES:
        try:
            # Call the API function with provided arguments
            return await api_func(*args, **kwargs)

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                retries += 1
                retry_after = int(e.response.headers.get("Retry-After", backoff))
                print(f"Rate limited. Retrying after {retry_after} seconds... ({retries}/{MAX_RETRIES})")
                await asyncio.sleep(retry_after)
                backoff *= 2  # Exponentially increase the backoff time
            else:
                raise  # Re-raise any other status code errors

    raise Exception("Max retries exceeded for API call.")


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


async def fetch_apex_leagues(queue="RANKED_SOLO_5x5", region="na1", api_key=API_KEY):
    """
    Fetches data from one of the apex leagues (Challenger, Grandmaster, or Master)
    ?? consider limiting the output to top 1700 players??
    """

    challenger_league = await fetch_challenger_leagues(queue=queue, region=region, api_key=api_key)
    grandmaster_league = await fetch_grandmaster_leagues(queue=queue, region=region, api_key=api_key)
    master_league = await fetch_master_leagues(queue=queue, region=region, api_key=api_key)

    leagues = [challenger_league, grandmaster_league, master_league]

    combined_ladder = []

    for league in leagues:
        tier = league.get("tier")
        for entry in league.get("entries", []):
            entry["tier"] = tier
            combined_ladder.append(entry)

    sorted_entries = sorted(combined_ladder, key=lambda x: x["leaguePoints"], reverse=True)

    return sorted_entries



async def fetch_account_ids(region="na1", summoner_id=None, api_key=API_KEY):
    if not summoner_id:
        raise ValueError("Summoner ID cannot be blank.")

    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}?api_key={api_key}"

    async def api_call():
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()

    return await backoff_api_call(api_call)


async def fetch_game_name_tagline(region="americas", puuid=None, api_key=API_KEY):
    if not puuid:
        raise ValueError("Puuid cannot be blank.")

    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={api_key}"

    async def api_call():
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()

    return await backoff_api_call(api_call)

async def fetch_game_name_tagline_all(region="americas", puuid_list=None, api_key=API_KEY):
    if not puuid_list:
        raise ValueError("puuid list cannot be blank.")
    game_name_tagline_all_list = []
    for puuid in puuid_list:
        try:
            api_data = await backoff_api_call(fetch_game_name_tagline, region=region, puuid=puuid, api_key=api_key)
            game_name_tagline_all_list.append(api_data)
        except Exception as e:
            print(f"Error fetching game_name_tagline for player puuid {puuid}: {e}")
            break

        await asyncio.sleep(RATE_LIMIT)  # Respect rate limiting between requests

    return game_name_tagline_all_list

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

    # for match_id in match_id_list:
    #     match_details = await fetch_match_details(region=region, match_id=match_id, api_key=API_KEY)
    #     match_details_all_list.append(match_details)
    #     await asyncio.sleep(RATE_LIMIT)
    #
    # return match_details_all_list
    for match_id in match_id_list:
        try:
            # Use backoff_api_call to fetch match details with retry logic
            match_details = await backoff_api_call(fetch_match_details, region=region, match_id=match_id,
                                                   api_key=api_key)
            match_details_all_list.append(match_details)
        except Exception as e:
            print(f"Error fetching match details for match ID {match_id}: {e}")
            break

        await asyncio.sleep(RATE_LIMIT)  # Respect rate limiting between requests

    return match_details_all_list


async def fetch_item_icons_ids():
    # Base URL for CommunityDragon assets
    base_url = "https://raw.communitydragon.org/latest/game/assets/items/icons2d/"
    items_url = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/items.json"

    # Use httpx to fetch the item metadata
    async with httpx.AsyncClient() as client:
        response = await client.get(items_url)
        items = response.json()

    # Create the directory to save icons if it doesn't exist
    project_root = Path(__file__).resolve().parent  # Get the directory of the current script
    icons_directory = project_root / '..' / '..' / '..' / 'frontend' / 'public' / 'icons' / 'items'  # Navigate to the desired directory
    icons_directory.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist

    print(f"Icons will be saved in: {icons_directory.resolve()}")  # Print the full path of the directory

    # Download each item icon and store it in the specified directory
    for item in items:
        item_id = item.get("id")
        item_name = item.get("name").replace(" ", "_")  # Replace spaces with underscores for filenames

        prefix = "/lol-game-data/assets/ASSETS/Items/Icons2D/"
        icon_path = item.get("iconPath")
        # Truncate icon_path
        if icon_path.startswith(prefix):
            icon_path = icon_path[len(prefix):]

        # Construct the full URL for the icon
        icon_url = f"{base_url}{icon_path.lstrip('/')}".lower()
        print(icon_url)

        # Define the filename for the icon
        sanitized_item_name = re.sub(r'[<>:"/\\|?*]', '_', item_name)  # Replace invalid characters
        icon_filename = f"item_{item_id}_{sanitized_item_name}.png"  # Create a unique filename
        icon_path_to_save = icons_directory / icon_filename  # Construct the full save path

        # Use httpx to download the icon
        async with httpx.AsyncClient() as client:
            icon_response = await client.get(icon_url)

            if icon_response.status_code == 200:
                # Check if the file already exists
                if icon_path_to_save.exists():
                    print(f"{icon_filename} already exists. Skipping download.")
                    continue  # Skip to the next item if the file exists

                # Save the icon to the specified directory
                with open(icon_path_to_save, 'wb') as icon_file:
                    icon_file.write(icon_response.content)
                print(f"Saved {icon_filename} to {icons_directory}")
            else:
                print(f"Failed to download {icon_filename}: {icon_response.status_code}")


