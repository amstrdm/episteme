import requests
from dotenv import load_dotenv
import os
import html
import re
from bs4 import BeautifulSoup
from datetime import datetime
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "../config/config.env")

load_dotenv(ENV_PATH)

"""
We use an unofficial RapidAPI here

Params: stock_ticker, num_posts

number of requests:
    1 + num_posts * (1 + 1)
    ^             ^      ^
    |             |      |   
Post List         |  Get contents of each comment inside list
                  |
        list of all comments   
""" 



base_url = "https://seeking-alpha.p.rapidapi.com"

headers = {
	"x-rapidapi-key": os.getenv("SEEKINGALPHA_RAPIDAPI_KEY"),
	"x-rapidapi-host": "seeking-alpha.p.rapidapi.com"
}



def find_seekingalpha_posts(stock_ticker, num_posts):
    url = f"{base_url}/analysis/v2/list"
    querystring = {"id":stock_ticker,"size":num_posts}
    response = requests.get(url, headers=headers, params=querystring)
    json_data = response.json()

    # Using a list comprehension to filter and collect IDs
    unlocked_posts = [post["id"] for post in json_data["data"] if not post["attributes"]["isLockedPro"]]
    return unlocked_posts

def clean_content(content):
    # Parse the HTML content
    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove script and style elements
    for script_or_style in soup(['script', 'style']):
        script_or_style.extract()
    
    # Get text and unescape HTML entities
    text = html.unescape(soup.get_text(separator=' ', strip=True))
    
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
        
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def get_top_comments(post_id, comment_limit=10):
    # First get the id of every comment on the specified post

    url_comment_list = f"{base_url}/comments/v2/list" 
    querystring_comments_list = {"id":post_id, "sort":"-top_parent_id"}
    response_comment_list = requests.get(url=url_comment_list, headers=headers, params=querystring_comments_list)
    json_data_comment_list = response_comment_list.json()
    comment_ids = [comment["id"] for comment in json_data_comment_list["data"]]
    
    # take the top 25% of comments
    filtered_comment_ids = comment_ids[:max(1, len(comment_ids) // 4)]
    
    # Limit the number of comments fetched if specified
    filtered_comment_ids = filtered_comment_ids[:comment_limit]

    # Get the content of each comment

    comment_texts = []
    url_comment_content = f"{base_url}/comments/get-contents"

    querystring_comments_content = {"id":post_id, "comment_ids":filtered_comment_ids}
    response_comment_content = requests.get(url=url_comment_content, headers=headers, params=querystring_comments_content)
    json_data_comment_content = response_comment_content.json()
    print(json_data_comment_content)
    for comment_data in json_data_comment_content["data"]:
        try:
            comment_content = comment_data["attributes"]["content"]
            comment = clean_content(comment_content)
            comment_texts.append(comment)
            print(comment_content)
        except IndexError: # Index error indicates the comment has no content in which case we'll ignore it
            print("No content found")
            pass
        
    

    return comment_texts

def get_seekingalpha_posts_info(stock_ticker, num_posts):
    url = f"{base_url}/analysis/v2/get-details"
    post_info_list = []
    
    post_ids = find_seekingalpha_posts(stock_ticker, num_posts)

    for post_id in post_ids:
        querystring = {"id":post_id}
        response = requests.get(url=url, headers=headers, params=querystring)
        json_data = response.json()

        title = json_data["data"]["attributes"]["title"]

        # Get author name by looping through "included" array since order is random
        author_name = None
        included_items = json_data.get("included", [])

        for item in included_items:
            if item.get("type") == "author":
                author_name = item.get('attributes', {}).get('nick')
                break

        # Convert time of post from iso to %d-%m-%Y
        time_of_post_iso = json_data["data"]["attributes"]["publishOn"]
        time_of_post_dt = datetime.fromisoformat(time_of_post_iso)
        time_of_post_formatted = time_of_post_dt.strftime("%d-%m-%Y")

        relative_url = json_data["data"]["links"]["self"]
        absolute_url = f"https://seekingalpha.com{relative_url}"

        unfiltered_content_list = json_data["data"]["attributes"]["summary"]
        unfiltered_content_str = ""
        for point in unfiltered_content_list:
            unfiltered_content_str += str(point)
        filtered_content = clean_content(unfiltered_content_str)

        comments = get_top_comments(post_id)

        post_info = {
            "title": title, 
            "author": author_name,
            "time_of_post": time_of_post_formatted,
            "url": absolute_url,
            "content": filtered_content,
            "comments": comments
        }
        post_info_list.append(post_info)

    return post_info_list



