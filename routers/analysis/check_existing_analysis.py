from database.db import SessionLocal
from database.models.thesisai import Ticker
from sqlalchemy import func

def check_ticker_in_database(ticker: str):
    session = SessionLocal()

    result = session.query(Ticker.symbol, Ticker.last_analyzed).filter(func.lower(Ticker.symbol) == ticker.lower()).first()
    return result.last_analyzed if result else None