#we need to scrape:
#1. Post Title
#2. author of post
#3. date of post
#4. post content
#5. top 25% of comments with a maximum limit of comments 
#6. upvotes of post 
#7. link of post

import json 
from datetime import datetime
import praw
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.getenv("ENV_PATH")
load_dotenv(ENV_PATH)

# we're gonna use praw to access the reddit api

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def find_reddit_posts(subreddit, stock_name, stock_ticker, timeframe, num_posts):
    try:
        # Fetch posts from the subreddit
        subreddit_instance = reddit.subreddit(subreddit)
        query = f"{stock_name} OR {stock_ticker}"
        posts = subreddit_instance.search(query, limit=num_posts, time_filter=timeframe)

        # Filter posts based on selftext length
        filtered_data = [post for post in posts if len(post.selftext) > 100]

        # if the post is from r/wallstreetbets we need to filter it out if it's not a DD 
        # we do that by checking if the posts flair is "DD"
        if subreddit == "wallstreetbets":
            filtered_data = [post for post in filtered_data if post.link_flair_text == "DD"]   
        return filtered_data
    except Exception as e:
        raise RuntimeError(f"Failed to fetch posts from subreddit '{subreddit}': {str(e)}") from e

def get_top_comments(submission, comment_limit=10):
    """
    Fetch the top comments for a given submission.
    """
    try:
        submission.comments.replace_more(limit=0)  # Load all comments, ignore 'MoreComments' objects
        comments = submission.comments.list()
        
        # Sort comments by score and take the top 25%
        sorted_comments = sorted(comments, key=lambda x: x.score, reverse=True)
        top_comments = sorted_comments[:max(1, len(sorted_comments) // 4)]
        
        # Limit the number of comments fetched if specified
        top_comments = top_comments[:comment_limit]
        
        comment_texts = []
        for comment in top_comments:
            comment_texts.append({
                "author": str(comment.author),
                "content": comment.body
            })
        return comment_texts
    except Exception as e:
        raise RuntimeError(f"Failed to fetch comments for post '{submission.id}': {str(e)}") from e


def get_reddit_posts_info(subreddits, stock_name, stock_ticker, timeframe, num_posts):
    try:
        post_info_list = []
        for subreddit in subreddits:
            posts = find_reddit_posts(subreddit, stock_name, stock_ticker, timeframe, num_posts)
            # we output title, author, date(which we have to convert from the unix timestamp), upvotes, and url of the post
            for post in posts:
                # Get top comments for each post
                top_comments = get_top_comments(post, comment_limit=10)

                # we save each post info as a dict then save them all in a list  
                # to later be converted into a pd dataframe
                post_info = {
                    "source": "reddit",
                    "subreddit": subreddit,
                    "title": post.title,
                    "author": str(post.author),
                    "time_of_post": datetime.fromtimestamp(post.created_utc).strftime('%d-%m-%Y'),
                    "upvotes": str(post.score),
                    "url": post.url,
                    "content": post.selftext,
                    "comments": top_comments
                }
                post_info_list.append(post_info)
        return post_info_list
    except Exception as e:
        raise RuntimeError(f"Failed to scrape Reddit posts: {str(e)}") from e

if __name__ == "__main__":
    # Example usage
    subreddits = ["stocks", "investing", "valueinvesting", "wallstreetbets"]
    stock_name = "Nubank"
    stock_ticker = "NU Holdings"
    timeframe = "year" #timeframe can be "hour", "day", "week", "month", "year", "all"
    num_posts = 1

    posts = get_reddit_posts_info(subreddits, stock_name, stock_ticker, timeframe, num_posts)

    for post in posts:
        print(json.dumps(post, indent=4), "\n\n")

