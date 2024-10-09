from pydantic import BaseModel
from ..db.models import Account
from ..models.league import League


def transform_league_to_accounts(league: League) -> list[Account]:
    accounts = []
    print("League data:", league)

    for entry in league['entries']:
        total_games = entry['wins'] + entry['losses']
        winrate = (entry['wins'] / total_games) * 100 if total_games > 0 else 0

        account = Account(
            summoner_id=entry['summonerId'],
            tier=league['tier'],
            league_points=entry['leaguePoints'],
            league_id=league['leagueId'],
            wins=entry['wins'],
            losses=entry['losses'],
            total_games=total_games,
            winrate=winrate,
        )
        accounts.append(account)

    return accounts