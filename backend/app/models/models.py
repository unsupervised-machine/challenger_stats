from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, Field, conint, constr, conlist


# noinspection DuplicatedCode
class AccountHistory(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))  # Generate a new ObjectId
    summoner_id: constr(min_length=1)  # Non-empty string
    tier: constr(min_length=1)  # Non-empty string
    league_points: conint(ge=0)  # Non-negative integer
    league_id: str
    wins: conint(ge=0)  # Non-negative integer
    losses: conint(ge=0)  # Non-negative integer
    total_games: conint(ge=0)  # Non-negative integer
    winrate: float  # Win rate can be any float value
    created_at: datetime = Field(default_factory=datetime.now)  # Timestamp for the entry


# noinspection DuplicatedCode
class AccountCurrent(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))  # Generate a new ObjectId
    summoner_id: constr(min_length=1)  # Non-empty string
    tier: constr(min_length=1)  # Non-empty string
    league_points: conint(ge=0)  # Non-negative integer
    league_id: str
    wins: conint(ge=0)  # Non-negative integer
    losses: conint(ge=0)  # Non-negative integer
    total_games: conint(ge=0)  # Non-negative integer
    winrate: float  # Win rate can be any float value
    created_at: datetime = Field(default_factory=datetime.now)  # Timestamp for the entry


class MatchData(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    match_id: constr(min_length=1)
    player_puuids: conlist(constr(min_length=1), min_length=10, max_length=10)
    player_champion: conlist(constr(min_length=1), min_length=10, max_length=10)
    player_kills: conlist(conint(ge=0), min_length=10, max_length=10)
    player_deaths: conlist(conint(ge=0), min_length=10, max_length=10)
    player_assists: conlist(conint(ge=0), min_length=10, max_length=10)