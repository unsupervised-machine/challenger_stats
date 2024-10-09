from pydantic import BaseModel

class Entry(BaseModel):
    summoner_id: str
    league_points: int
    rank: str
    wins: int
    losses: int
    veteran: bool
    inactive: bool
    fresh_blood: bool
    hot_streak: bool

class League(BaseModel):
    tier: str
    league_id: str
    queue: str
    name: str
    entries: list[Entry]  # Using built-in list type instead of List from typing

