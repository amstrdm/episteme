from .scraping import scrape_content
from sqlalchemy.orm import Session
from database.db import SessionLocal
from sqlalchemy import select
from typing import List, Dict
from database.models.thesisai import Ticker,  Post

# A simple in-memory store for tasks
# Keys = task_id, Value = dict with status, progress, error and result
TASKS = {}

def filter_already_analyzed_posts(
        session: Session,
        ticker_symbol: str,
        scraped_posts: List[Dict],
) -> List[Dict]:
    """
    Removes posts (from 'scraped_posts') that already exist in the DB
    for the given 'ticker_symbol'.
    
    Each element in 'scraped_posts' is assumed to be a dict with a 'url' field.
    """
    # 1. Find the Ticker row by symbol
    ticker = session.query(Ticker).filter_by(symbol=ticker_symbol).one_or_none()
    if not ticker:
        # create new Ticker
        ticker = Ticker(symbol=ticker_symbol.lower())
        session.add(ticker)
        session.commit()
        return scraped_posts
    # 2. Gather all scraped URLs in a set for quick membership checks
    scraped_urls = {post["url"] for post in scraped_posts if "url" in post}

    if not scraped_urls:
        # No URL's to filter
        return scraped_urls
    
    # 3. Retrieve existing URLs in one query
    stmt = (
        select(Post.link)
        .where(Post.ticker_id == ticker.id)
        .where(Post.link.in_(scraped_urls))
    )
    existing_links = set(link for (link,) in session.execute(stmt))

    # 4. Filter out scraped posts if their url is in 'existing_links'
    filtered_posts = [
        p for p in scraped_posts
        if p["url"] not in existing_links
    ]

    return filtered_posts

def start_analysis_process(
        # ticker:str,
        # title: str, 
        # subreddits: List[str], 
        # reddit_timeframe: str, 
        # reddit_num_posts: int, 
        # seekingalpha_num_posts: int, 
        # task_id: str,
        **kwargs,
    ):
    try:

        ticker = kwargs.get("ticker")
        task_id = kwargs.get("task_id")

        TASKS[task_id] = {
            "status": "Scraping content",
            "progress": 1,
            "ticker": ticker,
            "error": None
        }

        # Step 1: Scrape content
        kwargs.pop("task_id")
        scrape_results = scrape_content(**kwargs)
                
        # Update Task Status
        TASKS[task_id].update({
            "status": "filtering content",
            "progress": 2
        })

        # Step 2: Remove already analyzed posts from scraped posts
        filter_already_analyzed_posts(session=SessionLocal(), ticker_symbol=ticker, scraped_posts=scrape_results)

        # Step 3: Save scraped posts to Database
        

        # Update task status to completed
        TASKS[task_id].update({
            "status": "completed",
            "progress": 100,
        })

    except Exception as e:
        # Update task status as failed
        TASKS[task_id].update({
            "status": "failed",
            "error": str(e),
            "progress": 100, # Mark as fully progressed but failed
        })