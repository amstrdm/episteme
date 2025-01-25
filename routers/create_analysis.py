from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from pydantic import BaseModel
import uuid
from typing import Optional, List
from routers.analysis.run_analysis import TASKS, start_analysis_process
from dotenv import load_dotenv
import os

router = APIRouter()

ENV_PATH = os.getenv("ENV_PATH")
load_dotenv(ENV_PATH)
default_subreddits = os.getenv("REDDIT_DEFAULT_SUBREDDITS", "").split(",")
default_reddit_timeframe = os.getenv("REDDIT_DEFAULT_TIMEFRAME")
default_reddit_num_posts = os.getenv("REDDIT_DEFAULT_NUM_POSTS")

default_seekingalpha_num_posts = os.getenv("SEEKINGALPHA_DEFAULT_NUM_POSTS")

@router.get("/generate-analysis")
def start_analysis(
    background_tasks: BackgroundTasks,
    ticker:str = Query(..., description="The ticker symbol for the analysis"),
    title: str = Query(..., description="The stock name"),
    subreddits: Optional[List[str]] = Query(default=default_subreddits, description="List of subreddits to scrape"),
    reddit_timeframe: Optional[str] = Query(default=default_reddit_timeframe, description="Timeframe to scrape posts(e.g., 'hour', 'day', 'week', 'month', 'year', 'all')"),
    reddit_num_posts: Optional[int] = Query(default=default_reddit_num_posts, description="Number of reddit posts to scrape"),
    seekingalpha_num_posts: Optional[int] = Query(default=default_seekingalpha_num_posts, description="Number of seekingalpha posts to scrape")
    ):
    task_id = str(uuid.uuid4())

    # Initialize the task in the store with "pending" or "starting"
    TASKS[task_id] = {
        "status": "pending",
        "progress": 0,
        "ticker": ticker
    }

    # Add the analysis function to the background tasks
    background_tasks.add_task(start_analysis_process, ticker, title, subreddits, reddit_timeframe, reddit_num_posts, seekingalpha_num_posts, task_id)

    return {
        "message": f"Analysis for {ticker} started",
        "task_id": task_id,
        "status": "started"
    }

@router.get("/analysis-status")
def analysis_status(task_id: str):
    """
    Polling endpoint: user calls this with the task_id to check
    status and progress of the background job.
    """
    task = TASKS.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "status": task.get("status"),
        "progress": task.get("progress"),
        "error": task.get("error"),
        "ticker": task.get("ticker")
    }