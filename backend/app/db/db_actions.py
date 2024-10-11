from backend.app.models.models import Account, Match
from typing import List


class DatabaseActions:
    def __init__(self, db):
        self.db = db

    def insert_accounts(self, accounts: List[Account]):
        # might need change the format of the data either before it gets here or in this section
        self.db.accounts.insert_many(accounts)

    def insert_matches(self, matches: List[Match]):
        # might need change the format of the data either before it gets here or in this section
        self.db.matches.insert_many(matches)