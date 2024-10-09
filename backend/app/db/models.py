from sqlalchemy import Column, Integer, String, Float
# from sqlalchemy.ext.declarative import declarative_base
from .database import Base

# Base class for SQLAlchemy models
# Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)  # Primary key for the table
    summoner_id = Column(String, index=True)  # ID for the individual player
    tier = Column(String)  # e.g master
    league_points = Column(Integer)
    league_id = Column(String)  # ID for the league (NOT THE PLAYER)
    wins = Column(Integer)
    losses = Column(Integer)
    total_games = Column(Integer)
    winrate = Column(Float)

    def __repr__(self):
        return f"<Account(summoner_id={self.summoner_id}, tier={self.tier}, league_points={self.league_points}, wins={self.wins}, losses={self.losses}, total_games={self.total_games}, winrate={self.winrate})>"
