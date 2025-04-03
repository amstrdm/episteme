import logging
import numpy as np
from sqlalchemy import select
from typing import List, Dict
from sqlalchemy import func
import yfinance as yf
from datetime import datetime
import asyncio
from dateutil.relativedelta import relativedelta
from database.db import SessionLocal
from database.models.thesisai import Ticker, Post, Point
from .scraping import scrape_content
from .commit_filtered_posts import commit_posts_to_db
from .check_existing_analysis import check_ticker_in_database
from .ai.create_description import generate_company_description
from .ai.summarize_post import summarize_points_from_post
from .ai.filter_points import remove_duplicate_points

# A simple in-memory store for tasks
# Keys = task_id, Value = dict with status, progress, error and result
TASKS = {}

def add_new_ticker_to_db(ticker_symbol: str):
    print("Creating New Ticker")
    # Get Title of a stock by its ticker
    yf_ticker = yf.Ticker(ticker_symbol.lower())
    title = yf_ticker.info.get("longName", "N/A")
    
    with SessionLocal() as session:
        # Create new Ticker
        ticker = Ticker(
            symbol=ticker_symbol.lower(),
            name=title,
            description=generate_company_description(ticker_symbol.lower()),
            description_last_analyzed=datetime.now()
        )
        session.add(ticker)
        session.commit()

def update_description_if_needed(ticker_obj: Ticker):
    """
    Checks when the description saved in DB was generated.
    If it's been longer than 3 months it generates a new one.
    """
    last_analyzed = ticker_obj.description_last_analyzed
    three_months_ago = datetime.now() - relativedelta(months=3)

    if last_analyzed < three_months_ago:
        with SessionLocal() as session:
            generate_company_description(str(ticker_obj.symbol).lower())
            ticker_obj.description_last_analyzed = datetime.now()
            session.add(ticker_obj)
            session.commit()
        
def filter_analyzed_posts(
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
    with SessionLocal() as session:
        existing_links = set(link for (link,) in session.execute(stmt))

    # 3. Filter out scraped posts if their url is in 'existing_links'
    filtered_posts = [post for post in scraped_posts if post["url"] not in existing_links]

    return filtered_posts

async def summarize_all_posts(post_ids: List):
    tasks = [asyncio.create_task(summarize_points_from_post(pid)) for pid in post_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

def save_new_point(ticker_obj: Ticker, post_id: int, text: str, sentiment_score: int, embedding: np.array):
    """
    Save a new thesis point to the database, including its computed embedding.
    """
    with SessionLocal() as session:
        new_point = Point(
            ticker_id=ticker_obj.id,
            post_id=post_id,
            sentiment_score=sentiment_score,
            text=text,
            embedding=embedding.tolist()  # Convert numpy array to list for storage
        )
        session.add(new_point)
        session.commit()

async def start_analysis_process(
        # ticker:str,
        # title: str, 
        # subreddits: List[str], 
        # reddit_timeframe: str, 
        # reddit_num_posts: int, 
        # seekingalpha_num_posts: int, 
        # task_id: str,
        **kwargs,
    ):
    PROGRESS_STAGES = {
        0: "Initialization",
        1: "Updating company description",
        2: "Scraping content",
        3: "Filtering content",
        4: "Saving posts to database",
        5: "Extracting theses from posts",
        6: "Filtering out duplicate ideas",
    }
    try:
        ticker = kwargs.get("ticker").upper()
        task_id = kwargs.get("task_id")

        TASKS[task_id] = {
            "status": PROGRESS_STAGES[0],
            "progress": 0,
            "ticker": ticker,
            "error": None
        }

        print("Started analysis")
        ticker_exists, _ = check_ticker_in_database(ticker)
        print("TICKER EXISTS:", ticker_exists)
        if not ticker_exists:
            add_new_ticker_to_db(ticker)
        
        with SessionLocal() as session:
            ticker_obj = session.query(Ticker).filter(func.lower(Ticker.symbol) == ticker.lower()).first()

        # Step 1: Generate Description
        TASKS[task_id].update({
            "status": PROGRESS_STAGES[1],
            "progress": 1
        })
        update_description_if_needed(ticker_obj)

        # Step 2: Scrape content
        TASKS[task_id].update({
            "status": PROGRESS_STAGES[2],
            "progress": 2
        })
        kwargs.pop("task_id")
        scrape_results = scrape_content(**kwargs)
        
        # Step 3: Remove posts that are already in database and have therefore been analyzed before from scraped posts
        TASKS[task_id].update({
            "status": PROGRESS_STAGES[3],
            "progress": 3
        })
        filtered_posts = filter_analyzed_posts(ticker_obj=ticker_obj, scraped_posts=scrape_results)

        # Step 4: Save scraped posts to Database
        TASKS[task_id].update({
            "status": PROGRESS_STAGES[4],
            "progress": 4
        })
        new_posts_ids = commit_posts_to_db(posts_data=filtered_posts, ticker_symbol=ticker, SessionLocal=SessionLocal)
        
        # Step 5: Summarize saved posts
        TASKS[task_id].update({
            "status": PROGRESS_STAGES[5],
            "progress": 5
        })
        summarization_results = await summarize_all_posts(new_posts_ids)
        new_points = []
        for result in summarization_results:
            if isinstance(result, Exception):
                logging.warning("Instance of Summarization Step failed:", result)
                continue
            new_points.append(result)
        
        # Step 6: Filter out duplicate points
        TASKS[task_id].update({
            "status": PROGRESS_STAGES[6],
            "progress": 6
        })

        # for new_p in new_points:
        #    remove_duplicate_points(new_points=new_p, ticker_obj=ticker_obj)
        # Step 5: 
        # Update task status to completed
        TASKS[task_id].update({
            "status": "completed",
            "progress": 100,
        })
        print(TASKS[task_id])

        with SessionLocal() as session:
            ticker_obj.last_analyzed = datetime.now()
            session.commit()

    except Exception as e:
        error_stage = TASKS[task_id].get("status")
        
        # Log the detailed error information to the log file
        logging.error(f"Analysis failed for task {task_id}, ticker: {ticker}. Error occurred during {error_stage}: {str(e)}", exc_info=True)

        # Update task with user-friendly error message
        TASKS[task_id].update({
            "status": "failed",
            "error": f"An error occurred during {error_stage}. Please try again later or contact support.",
            "progress": 100, # Mark as fully progressed but failed
        })