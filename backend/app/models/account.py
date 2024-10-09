from pydantic import BaseModel

class Account(BaseModel):
    summonerId: str     # ID for the individual player
    tier: str           # e.g master
    leaguePoints: int
    leagueId: str       # ID for the league ( NOT THE PLAYER )
    wins: int
    losses: int
    totalGames: int
    winrate: float

    # favorite_champions: List
    # average_kills: float
    # average_deaths: float
    # average_assists: floats
