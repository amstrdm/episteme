from concurrent.futures import ThreadPoolExecutor, as_completed
from .scrapers.reddit_scraper import get_reddit_posts_info
from .scrapers.seekingalpha_scraper import get_seekingalpha_posts_info

def scrape_reddit(ticker:str, title: str, subreddits, reddit_timeframe: str, reddit_num_posts: int):
    return get_reddit_posts_info(stock_ticker=ticker, stock_name=title, subreddits=subreddits, timeframe=reddit_timeframe, num_posts=reddit_num_posts)

def scrape_seekingalpha(ticker:str, seekingalpha_num_posts: int):
    return get_seekingalpha_posts_info(stock_ticker=ticker, num_posts=seekingalpha_num_posts)

def scrape_content(ticker:str, title: str, subreddits, reddit_timeframe: str, reddit_num_posts: int, seekingalpha_num_posts):
    # Create a thread pool
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_to_name = {
            executor.submit(scrape_reddit, ticker, title, subreddits, reddit_timeframe, reddit_num_posts): "reddit",
            executor.submit(scrape_seekingalpha, ticker, seekingalpha_num_posts): "seekingalpha"
        }

        # As they complete gather results
        results = {}
        for future in as_completed(future_to_name):
            source_name = future_to_name[future]
            try:
                data = future.result()
                results[source_name] = data
            except Exception as e:
                print(f"Error scraping {source_name}: {e}")
                raise f"Error scraping {source_name}: {e}"
                #! Have to implement error handling here to raise possible scraping errors to run_analysis which should then raise to frontend
    # 'results' now holds data from both threads
    reddit_data = results.get("reddit", [])
    seekingalpha_data = results.get("seekingalpha", [])

    print("== REDDIT DATA ==")
    for post in reddit_data:
        print(post)
    
    print("\n== SEEKINGALPHA DATA ==")
    for post in seekingalpha_data:
        print(post)

    return [reddit_data, seekingalpha_data]

if __name__ == "__main__":
    scrape_content(ticker="VST", title="Vistra", subreddits=["stocks", "investing", "valueinvesting", "wallstreetbets"], reddit_timeframe="year", reddit_num_posts=1, seekingalpha_num_posts=1)