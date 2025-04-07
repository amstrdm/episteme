from database.models.thesisai import Ticker, Point
from database.db import session_scope

def calculate_ticker_sentiment(ticker_id: int):
    with session_scope() as session:
        point_objs = session.query(Point).filter(Point.ticker_id == ticker_id).all()
        sentiment_scores = [point.sentiment_score for point in point_objs]
    if len(sentiment_scores) > 0:
        average_score = sum(sentiment_scores) / len(sentiment_scores)
    else:
        average_score = 0
    return average_score

