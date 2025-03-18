from database.db import SessionLocal
from database.models.thesisai import Ticker
from sqlalchemy import func


def check_ticker_in_database(ticker: str):
    
    with SessionLocal() as session:
        result = session.query(Ticker.last_analyzed).filter(func.lower(Ticker.symbol) == ticker.lower()).first()

    if result is not None:
        return True, result[0]
    else:
        return False, None