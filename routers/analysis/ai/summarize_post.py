from database.db import SessionLocal
from database.models.thesisai import Post

session = SessionLocal()

def summarize_points_from_post(post_id):
    prompt = """
    Read the following investment post and extract only the one-line thesis points that state why the stock is good (bullish) or bad (bearish). Each extracted point must be a single, concise sentence that directly presents a key investment thesis. If there are no clearly defined bullish or bearish thesis points, return nothing.
    """
    post = session.query(Post).filter(Post.id == post_id).first()
