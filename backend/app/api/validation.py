from pydantic import BaseModel
from typing import List
from datetime import datetime

class LeagueEntry(BaseModel):
    summonerId: str
    leaguePoints: int
    rank: str
    wins: int
    losses: int
    veteran: bool
    inactive: bool
    freshBlood: bool
    hotStreak: bool

class League(BaseModel):
    tier: str
    leagueId: str
    queue: str
    name: str
    entries: List[LeagueEntry]
    added_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "tier": "Diamond",
                "leagueId": "123abc",
                "queue": "RANKED_SOLO_5x5",
                "name": "The Best League",
                "entries": [
                    {
                        "summonerId": "summoner123",
                        "leaguePoints": 250,
                        "rank": "I",
                        "wins": 150,
                        "losses": 100,
                        "veteran": True,
                        "inactive": False,
                        "freshBlood": False,
                        "hotStreak": True
                    }
                ],
                "added_at": "2024-10-11T12:00:00"
            }
        }