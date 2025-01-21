from scraping import scrape_content

# A simple in-memory store for tasks
# Keys = task_id, Value = dict with status, progress, and result
TASKS = {}

def start_analysis_process(ticker:str, title: str, subreddits, reddit_timeframe: str, reddit_num_posts: int, seekingalpha_num_posts, task_id: str):
    TASKS[task_id] = {
        "status": "Started Analysis",
        "progress": 0,
        "ticker": ticker,
    }

    TASKS[task_id] = {
        "status": "Scraping Content",
        "progress": 1,
        "ticker": ticker,
    }

    scrape_results = scrape_content(ticker=ticker, title=title, subreddits=subreddits, reddit_timeframe=reddit_timeframe, reddit_num_posts=reddit_num_posts, seekingalpha_num_posts=seekingalpha_num_posts)
    
    # Have to implement error handling here to raise possible scraping errors to the frontend
    
    # Once done, update the status and store a "result"
    TASKS[task_id]["status"] = "completed"