from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models.thesisai import Post, Ticker
from .check_existing_analysis import check_ticker_in_database


def commit_posts_to_db(
        posts_data: List[Dict],
        ticker_symbol: str,
        SessionLocal: Session
        ):
    with SessionLocal() as session:
        # We shouldn't have to do this since it's already done when filtering out posts in run_analysis but better safe than sorry.    
        ticker_exists, _ = check_ticker_in_database(ticker_symbol)
        if not ticker_exists:
            # create new Ticker
            ticker_obj = Ticker(symbol=ticker_symbol.lower())
            session.add(ticker_obj)
            session.commit()
        else:
            ticker_obj = session.query(Ticker).filter(func.lower(Ticker.symbol) == ticker_symbol.lower()).first()

        new_post_ids = []
        for post in posts_data:
            new_post = Post(
                ticker_id=ticker_obj.id,
                source=post.get("source"),
                title=post.get("title", ""),
                link=post.get("url"),
                content=post.get("content")
            )
            session.add(new_post)
            session.flush()
            new_post_ids.append(new_post.id)
        session.commit()
    
    return new_post_ids
