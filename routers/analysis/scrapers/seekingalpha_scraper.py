import requests
from dotenv import load_dotenv
import os
import html
import re
from bs4 import BeautifulSoup
from datetime import datetime
import json
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.getenv("ENV_PATH")

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


def get_json_response(response, expected_keys=None):
    """
    Convert response to JSON and verify that expected_keys are present.
    If expected_keys is provided and any key is missing, raise an error with the full JSON.
    """
    try:
        json_data = response.json()
    except Exception as e:
        raise RuntimeError(f"Invalid JSON response: {response.text}") from e

    if expected_keys:
        missing_keys = [key for key in expected_keys if key not in json_data]
        if missing_keys:
            formatted_json = json.dumps(json_data, indent=4)
            raise RuntimeError(
                f"Unexpected response format. Missing keys: {missing_keys}. Full response:\n{formatted_json}"
            )

    return json_data


def find_seekingalpha_posts(stock_ticker, num_posts):
    try:
        url = f"{base_url}/analysis/v2/list"
        querystring = {"id": stock_ticker, "size": num_posts}
        response = requests.get(url, headers=headers, params=querystring)
        # Validate response has a "data" key
        json_data = get_json_response(response, expected_keys=["data"])

        # Using a list comprehension to filter and collect IDs
        unlocked_posts = [
            post["id"]
            for post in json_data["data"]
            if not post["attributes"].get("isLockedPro", True)
        ]
        return unlocked_posts
    except Exception as e:
        raise RuntimeError(f"Failed to fetch SeekingAlpha posts: {str(e)}") from e


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


def get_top_comments(post_id, post_url, comment_limit=10):
    try:
        # First get the id of every comment on the specified post
        url_comment_list = f"{base_url}/comments/v2/list"
        querystring_comments_list = {"id": post_id, "sort": "-top_parent_id"}
        response_comment_list = requests.get(
            url=url_comment_list, headers=headers, params=querystring_comments_list
        )
        json_data_comment_list = get_json_response(response_comment_list, expected_keys=["data"])
        comment_ids = [comment["id"] for comment in json_data_comment_list["data"]]

        # Take the top 25% of comments
        filtered_comment_ids = comment_ids[:max(1, len(comment_ids) // 4)]

        # Limit the number of comments fetched if specified
        filtered_comment_ids = filtered_comment_ids[:comment_limit]

        # Get the content of each comment
        comment_texts = []
        url_comment_content = f"{base_url}/comments/get-contents"
        querystring_comments_content = {"id": post_id, "comment_ids": filtered_comment_ids}
        response_comment_content = requests.get(
            url=url_comment_content, headers=headers, params=querystring_comments_content
        )
        json_data_comment_content = get_json_response(response_comment_content, expected_keys=["data"])

        for comment_data in json_data_comment_content["data"]:
            try:
                comment_content_raw = comment_data["attributes"]["content"]
                comment_content = clean_content(comment_content_raw)
                comment_url = post_url + "#comment-" + comment_data["id"]

                comment = {
                    "content": comment_content,
                    "url": comment_url
                }
                comment_texts.append(comment)
            except (IndexError, KeyError):
                # Index error or missing key indicates the comment has no content; ignore it.
                print("No content found for a comment; skipping.")
                continue

        return comment_texts
    except Exception as e:
        raise RuntimeError(f"Failed to fetch comments for post '{post_id}': {str(e)}") from e


def get_seekingalpha_posts_info(stock_ticker, num_posts):
    url = f"{base_url}/analysis/v2/get-details"
    post_info_list = []
    try:
        post_ids = find_seekingalpha_posts(stock_ticker, num_posts)
    except Exception as e:
        # Log error if we can't even fetch the list of post IDs
        raise RuntimeError(f"Failed to fetch SeekingAlpha posts for ticker {stock_ticker}: {str(e)}") from e

    for post_id in post_ids:
        try:
            querystring = {"id": post_id}
            response = requests.get(url=url, headers=headers, params=querystring)
            json_data = get_json_response(response, expected_keys=["data"])

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
            unfiltered_content_str = "".join(str(point) for point in unfiltered_content_list)
            filtered_content = clean_content(unfiltered_content_str)

            comments = get_top_comments(post_id=post_id, post_url=absolute_url)

            post_info = {
                "source": "seekingalpha",
                "title": title,
                "author": author_name,
                "time_of_post": time_of_post_formatted,
                "url": absolute_url,
                "content": filtered_content,
                "comments": comments
            }
            post_info_list.append(post_info)
        except Exception as e:
            # Log the error for this particular post and continue with the next
            logging.warning(f"Skipping post {post_id} due to error: {e}")
            continue

    return post_info_list


if __name__ == "__main__":
    posts = get_seekingalpha_posts_info(stock_ticker="aapl", num_posts=5)
    for post in posts:
        print(json.dumps(post, indent=4))
