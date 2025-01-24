from .scraping import scrape_content
from sqlalchemy.orm import Session
from database.db import SessionLocal
from sqlalchemy import select
from typing import List, Dict
from database.models.thesisai import Ticker,  Post

# A simple in-memory store for tasks
# Keys = task_id, Value = dict with status, progress, and result
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

def start_analysis_process(ticker:str, title: str, subreddits, reddit_timeframe: str, reddit_num_posts: int, seekingalpha_num_posts, task_id: str):
    TASKS[task_id] = {
        "status": "Started Analysis",
        "progress": 0,
        "ticker": ticker,
    }

    TASKS[task_id] = {
        "status": "Scraping content",
        "progress": 1,
        "ticker": ticker,
    }

    # Step 1: Scrape content
    scrape_results = scrape_content(
        ticker=ticker,
        title=title, 
        subreddits=subreddits, 
        reddit_timeframe=reddit_timeframe, 
        reddit_num_posts=reddit_num_posts, 
        seekingalpha_num_posts=seekingalpha_num_posts
    )
    
    # Have to implement error handling here to raise possible scraping errors to the frontend
    
    TASKS[task_id]["status"] = "Filtering out content"
    TASKS[task_id]["progress"] = "2"

    # Step 2: Remove already analyzed posts from scraped posts
    filter_already_analyzed_posts(session=SessionLocal(), ticker_symbol=ticker, scraped_posts=scrape_results)


    # Once done, update the status and store a "result"
    TASKS[task_id]["status"] = "completed"