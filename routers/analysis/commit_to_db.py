from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models.thesisai import Post, Ticker, Comment
from database.db import SessionLocal
from database.models.thesisai import Point, Criticism
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

            for comment in post.get("comments"):
                new_comment = Comment(
                    content = comment.get("content"),
                    link = comment.get("url"),
                    author = comment.get("author", None)
                )
                new_post.comments.append(new_comment)            
            
            new_post_ids.append(new_post.id)
        session.commit()
    
    return new_post_ids

def commit_final_points_to_db(points_list: list[dict]):        
    if not points_list:
        return
    
    with SessionLocal() as session:
        post_obj = session.query(Post).filter(Post.id == points_list[0].get("post_id")).first() # Doesnt't matter which post we query since they all have the same ticker.id
        ticker_id = post_obj.ticker_id

        for pt_data in points_list:
            new_point = Point(
                ticker_id = ticker_id,
                post_id = pt_data.get("post_id"),
                sentiment_score = pt_data.get("sentiment_score"),
                text = pt_data.get("point"),
                criticism_exists = pt_data.get("criticism_exists"),
                embedding = pt_data.get("embedding")
            )

            for crit_data in pt_data.get("criticisms", []):
                new_criticism = Criticism(
                    comment_id = crit_data.get("comment_id"),
                    text = crit_data.get("criticism"),
                    validity_score = crit_data.get("validity_score"),
                )

                new_point.criticisms.append(new_criticism)
            session.add(new_point)
        session.commit()

def commit_overall_sentiment_score(ticker_id: int, overall_sentiment_score: int):
    with SessionLocal() as session:
        ticker_obj = session.get(Ticker, ticker_id)
        ticker_obj.overall_sentiment_score = overall_sentiment_score
        session.commit()

