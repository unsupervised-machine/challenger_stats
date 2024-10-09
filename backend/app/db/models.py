from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class AccountHistory(Base):
    __tablename__ = "accountsHistory"

    id = Column(Integer, primary_key=True, index=True)
    summoner_id = Column(String, index=True)
    tier = Column(String)
    league_points = Column(Integer)
    league_id = Column(String)
    wins = Column(Integer)
    losses = Column(Integer)
    total_games = Column(Integer)
    winrate = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Timestamp for the entry

    def __repr__(self):
        return f"<AccountHistory(summoner_id={self.summoner_id}, tier={self.tier}, league_points={self.league_points}, wins={self.wins}, losses={self.losses}, total_games={self.total_games}, winrate={self.winrate})>"


class AccountCurrent(Base):
    __tablename__ = "accountsCurrent"

    id = Column(Integer, primary_key=True, index=True)
    summoner_id = Column(String, index=True)
    tier = Column(String)
    league_points = Column(Integer)
    league_id = Column(String)
    wins = Column(Integer)
    losses = Column(Integer)
    total_games = Column(Integer)
    winrate = Column(Float)
    run_timestamp = Column(DateTime(timezone=True), server_default=func.now())  # Timestamp for the run

    def __repr__(self):
        return f"<AccountCurrent(summoner_id={self.summoner_id}, tier={self.tier}, league_points={self.league_points}, wins={self.wins}, losses={self.losses}, total_games={self.total_games}, winrate={self.winrate})>"
