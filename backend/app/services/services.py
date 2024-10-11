from backend.app.db.db_actions import DatabaseActions
from backend.app.models.models import Account

import httpx
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("DEFAULT_RIOT_API_KEY")


class AccountService:
    def __init__(self, db_actions: DatabaseActions):
        self.db_actions = db_actions

