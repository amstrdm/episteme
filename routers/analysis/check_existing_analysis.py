from database.db import SessionLocal
from database.models.thesisai import Ticker


def check_ticker_in_database(ticker: str):
    session = SessionLocal()

    result = session.query(Ticker.symbol, Ticker.last_analyzed).filter(Ticker.symbol == ticker).first()
    return result.last_analyzed if result else None