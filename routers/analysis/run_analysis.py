from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Dict
from sqlalchemy import func
from datetime import datetime
from database.db import SessionLocal
from database.models.thesisai import Ticker, Post
from .scraping import scrape_content
from .commit_filtered_posts import commit_posts_to_db
from .check_existing_analysis import check_ticker_in_database
from database.models.stock_index import stocks_table

# A simple in-memory store for tasks
# Keys = task_id, Value = dict with status, progress, error and result
TASKS = {}

def add_new_ticker_to_db(ticker_symbol: str):
    print("Creating New Ticker")
    # Get Title of a stock by its ticker
    with SessionLocal() as session:
        stmt = select(stocks_table.c.title).where(func.lower(stocks_table.c.ticker) == ticker_symbol.lower())
        title = session.execute(stmt).scalar()
    
    # create new Ticker
    ticker = Ticker(
        symbol=ticker_symbol.lower(),
        name=title,
    )
    session.add(ticker)
    session.commit()


def filter_analyzed_posts(
        session: Session,
        ticker_obj: str,
        scraped_posts: List[Dict],
) -> List[Dict]:
    """
    Removes posts (from 'scraped_posts') that already exist in the DB
    for the given 'ticker_symbol'.
    
    Each element in 'scraped_posts' is assumed to be a dict with a 'url' field.
    """
    # 1. Gather all scraped URLs in a set for quick membership checks
    scraped_urls = {post["url"] for post in scraped_posts if "url" in post}

    if not scraped_urls:
        # No URL's to filter
        return scraped_urls
    
    # 2. Retrieve existing URLs in one query
    stmt = (
        select(Post.link)
        .where(Post.ticker_id == ticker_obj.id)
        .where(Post.link.in_(scraped_urls))
    )
    existing_links = set(link for (link,) in session.execute(stmt))

    # 3. Filter out scraped posts if their url is in 'existing_links'
    filtered_posts = [post for post in scraped_posts if post["url"] not in existing_links]

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
        print("Started analysis")
        ticker = kwargs.get("ticker").upper()
        task_id = kwargs.get("task_id")

        session = SessionLocal()

        ticker_exists, _ = check_ticker_in_database(ticker)
        print("TICKER EXISTS:", ticker_exists)
        if not ticker_exists:
            add_new_ticker_to_db(ticker)
        
        ticker_obj = session.query(Ticker).filter(func.lower(Ticker.symbol) == ticker.lower()).first()

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
        # Step 2: Remove posts that are already in database and have therefore been analyzed before from scraped posts
        filtered_posts = filter_analyzed_posts(session=SessionLocal(), ticker_obj=ticker_obj, scraped_posts=scrape_results)

        TASKS[task_id].update({
            "status": "saving posts to database",
            "progress": 3
        })

        # Step 3: Save scraped posts to Database
        new_posts_ids = commit_posts_to_db(posts_data=filtered_posts, ticker_symbol=ticker, session=SessionLocal())

        # Update task status to completed
        TASKS[task_id].update({
            "status": "completed",
            "progress": 100,
        })
        print(TASKS[task_id])

        ticker_obj.last_analyzed = datetime.now()
        session.commit()

    except Exception as e:
        # Update task status as failed
        TASKS[task_id].update({
            "status": "failed",
            "error": str(e),
            "progress": 100, # Mark as fully progressed but failed
        })