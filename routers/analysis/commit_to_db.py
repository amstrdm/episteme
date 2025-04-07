import logging
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from database.models.thesisai import Post, Ticker, Comment, Point, Criticism
from database.db import session_scope
from .check_existing_analysis import check_ticker_in_database



def convert_str_to_datetime(date_str: str) -> datetime:
    dt_object = datetime.strptime(date_str, "%d-%m-%Y")
    formatted_date = dt_object.strftime("%Y-%m-%d %H:%M")
    return formatted_date


def commit_posts_to_db(
        posts_data: List[Dict],
        ticker_symbol: str,
        session_scope: Session
        ):
    with session_scope() as session:
        # Ensure the Ticker exists.
        ticker_exists, _ = check_ticker_in_database(ticker_symbol)
        if not ticker_exists:
            ticker_obj = Ticker(symbol=ticker_symbol.lower())
            session.add(ticker_obj)
            session.flush()  # flush to generate an id
        else:
            ticker_obj = session.query(Ticker).filter(
                func.lower(Ticker.symbol) == ticker_symbol.lower()
            ).first()

        new_post_ids = []
        for post in posts_data:
            try:
                # Use a nested transaction so that failures here don't roll back the entire outer transaction.
                with session.begin_nested():
                    new_post = Post(
                        ticker_id=ticker_obj.id,
                        source=post.get("source"),
                        title=post.get("title", ""),
                        author=post.get("author", None),
                        link=post.get("url"),
                        content=post.get("content"),
                        date_of_post=convert_str_to_datetime(post.get("time_of_post"))
                                      if post.get("time_of_post") else None
                    )
                    session.add(new_post)
                    session.flush()  # to assign an id

                    for comment in post.get("comments", []):
                        new_comment = Comment(
                            content=comment.get("content"),
                            link=comment.get("url"),
                            author=comment.get("author", None)
                        )
                        new_post.comments.append(new_comment)

                    new_post_ids.append(new_post.id)
            except Exception as e:
                logging.warning(
                    "Error processing post with URL %s: %s", post.get("url"), str(e)
                )
                continue
    return new_post_ids


def commit_final_points_to_db(points_list: List[Dict]):
    if not points_list:
        return

    with session_scope() as session:
        # We assume that all points are for posts with the same ticker.
        post_obj = session.query(Post).filter(
            Post.id == points_list[0].get("post_id")
        ).first()
        ticker_id = post_obj.ticker_id

        for pt_data in points_list:
            try:
                with session.begin_nested():
                    new_point = Point(
                        ticker_id=ticker_id,
                        post_id=pt_data.get("post_id"),
                        sentiment_score=pt_data.get("sentiment_score"),
                        text=pt_data.get("point"),
                        criticism_exists=pt_data.get("criticism_exists"),
                        embedding=pt_data.get("embedding")
                    )

                    for crit_data in pt_data.get("criticisms", []):
                        new_criticism = Criticism(
                            comment_id=crit_data.get("comment_id"),
                            text=crit_data.get("criticism"),
                            validity_score=crit_data.get("validity_score"),
                        )
                        new_point.criticisms.append(new_criticism)

                    session.add(new_point)
            except Exception as e:
                logging.warning(
                    "Error processing point for post %s: %s", pt_data.get("post_id"), str(e)
                )
                continue


def commit_overall_sentiment_score(ticker_id: int, overall_sentiment_score: int):
    with session_scope() as session:
        ticker_obj = session.get(Ticker, ticker_id)
        ticker_obj.overall_sentiment_score = overall_sentiment_score
        session.commit()
