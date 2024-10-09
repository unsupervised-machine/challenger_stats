from sqlalchemy.orm import Session
# from backend.app.db.models import Account
from backend.app.db.models import AccountHistory, AccountCurrent

def insert_accounts_history(db: Session, accounts: list[AccountHistory]):
    # Insert all accounts into the AccountHistory table
    historic_accounts = [
        AccountHistory(
            summoner_id=account.summoner_id,
            tier=account.tier,
            league_points=account.league_points,
            league_id=account.league_id,
            wins=account.wins,
            losses=account.losses,
            total_games=account.total_games,
            winrate=account.winrate
        ) for account in accounts
    ]
    db.add_all(historic_accounts)
    db.commit()

def create_accounts_current(db: Session, accounts: list[AccountCurrent]):
    # Clear previous run data
    db.query(AccountCurrent).delete()  # Clear the current accounts table
    db.commit()

    # Insert new accounts into the AccountCurrent table
    current_accounts = [
        AccountCurrent(
            summoner_id=account.summoner_id,
            tier=account.tier,
            league_points=account.league_points,
            league_id=account.league_id,
            wins=account.wins,
            losses=account.losses,
            total_games=account.total_games,
            winrate=account.winrate
        ) for account in accounts
    ]
    db.add_all(current_accounts)
    db.commit()

#
# # Create a new account
# def create_account(db: Session, account: Account):
#     db.add(account)
#     db.commit()
#     db.refresh(account)
#     return account
#
#
#
#
# # Get an account by summoner ID
# def get_account(db: Session, summoner_id: str):
#     return db.query(Account).filter(Account.summoner_id == summoner_id).first()
#
# # Get all accounts
# def get_accounts(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(Account).offset(skip).limit(limit).all()
#
# # Update an account
# def update_account(db: Session, summoner_id: str, updated_account: Account):
#     account = db.query(Account).filter(Account.summoner_id == summoner_id).first()
#     if account:
#         account.tier = updated_account.tier
#         account.league_points = updated_account.league_points
#         account.league_id = updated_account.league_id
#         account.wins = updated_account.wins
#         account.losses = updated_account.losses
#         account.total_games = updated_account.total_games
#         account.winrate = updated_account.winrate
#         db.commit()
#         db.refresh(account)
#         return account
#     return None
#
# # Delete an account
# def delete_account(db: Session, summoner_id: str):
#     account = db.query(Account).filter(Account.summoner_id == summoner_id).first()
#     if account:
#         db.delete(account)
#         db.commit()
#         return True
#     return False
