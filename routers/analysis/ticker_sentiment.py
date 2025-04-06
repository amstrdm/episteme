from database.models.thesisai import Ticker, Point
from database.db import session_scope

def calculate_ticker_sentiment(ticker_obj: Ticker):
    with session_scope() as session:
        points = session.query(Point).filter(Point.ticker_id == ticker_obj.id).all()

    sentiment_scores = [point.sentiment_score for point in points]
    average_score = sum(sentiment_scores) / len(sentiment_scores)

    return average_score

