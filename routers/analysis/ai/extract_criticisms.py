from collections import defaultdict
from database.db import session_scope
from database.models.thesisai import Comment
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import json
import asyncio

ENV_PATH = os.getenv("ENV_PATH")
load_dotenv(ENV_PATH)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY ENVIRONMENT VARIABLE IS EITHER EMPTY OR DOESN'T EXIST")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def process_post_group(post_id: int, points: list, ticker_symbol: str = "", ) -> list:
    """
    For a single post, fetch the comments and use GPT to analyze the minimal version of each thesis point.
    The minimal version only contains 'point' and 'sentiment_score'.
    GPT returns for each point its analysis (whether a criticism exists and what criticisms, if any).
    Then we merge GPT's output with the original full data (which might include embedding, post_id, etc.)
    by matching on 'point' and 'sentiment_score'.
    """

    with session_scope() as session:
        comment_objs = session.query(Comment).filter(Comment.post_id == post_id).all()
        comments_data = [{"comment_id": comment.id, "content": comment.content} for comment in comment_objs]

    # Create a minimal version of the points: only include text and sentiment.
    minimal_points = [
        {"point": p["point"], "sentiment_score": p["sentiment_score"]}
        for p in points
    ]

    system_prompt = (
        "You are a financial analysis assistant. You are given an array of minimal thesis points (each with 'point' and 'sentiment_score'), "
        "an array of comment objects (each with 'comment_id' and 'content'), and the ticker of the stock the post is about. "
        "You are allowed to use the web to validate criticisms if needed.\n\n"
        "For each thesis point, do the following:\n"
        "1. If no valid criticism is found in the comments, output an object with 'criticism_exists' set to false and 'criticisms' as an empty array.\n"
        "2. If valid criticism(s) is found and the point remains viable, output the point with 'criticism_exists' set to true and attach a very succinct, headline-style summarized version of each criticism along with a validity score (an integer from 1 to 100) and include the 'comment_id' from which that criticism is derived. Avoid extra verbiage; provide only the essential summary.\n"
        "3. If multiple strong criticisms are present, or if any criticism is so strong that it completely invalidates the point (especially if confirmed via web validation), do not include that point in the output.\n\n"
    )

    user_prompt = (
       # f"Ticker: {ticker_symbol}\n"
        f"Points: {json.dumps(minimal_points, indent=2)}\n"
        f"Comments: {json.dumps(comments_data, indent=2)}"
    )
    
    response = await client.responses.create(
        model="o3-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
       # tools=[{"type": "web_search_preview"}],
        text={
            "format": {
                "type": "json_schema",
                "name": "comment_analysis",
                "schema": {
                    "type": "object",
                    "properties": {
                        "results": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "point": {"type": "string"},
                                    "sentiment_score": {"type": "integer"},
                                    "criticism_exists": {"type": "boolean"},
                                    "criticisms": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "criticism": {"type": "string"},
                                                "validity_score": {"type": "integer"},
                                                "comment_id": {"type": "integer"}
                                            },
                                            "required": ["criticism", "validity_score", "comment_id"],
                                            "additionalProperties": False
                                        }
                                    }
                                },
                                "required": ["point", "sentiment_score", "criticism_exists", "criticisms"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["results"],
                    "additionalProperties": False
                }
            }
        }
    )


    gpt_response = json.loads(response.output_text)
    gpt_analysis = gpt_response.get("results", [])
    # Merge GPT's analysis with the original full points by matching on 'point' and 'sentiment_score'.
    merged_points = []
    for orig in points:
        for analysis in gpt_analysis:
            if analysis["point"] == orig["point"] and analysis["sentiment_score"] == orig["sentiment_score"]:
                merged = orig.copy()
                merged.update(analysis)
                merged_points.append(merged)
                break

    return merged_points

async def analyze_comments(ticker_symbol: str, points_list: list) -> list:
    """
    Group points by post_id, process each group concurrently, and return a flat list of merged point dictionaries.
    """
    grouped_points = defaultdict(list)
    for point in points_list:
        grouped_points[point["post_id"]].append(point)
    
    tasks = []
    
    for post_id, pts in grouped_points.items():
        tasks.append(process_post_group(post_id, pts, ticker_symbol))
    
    results_per_post = await asyncio.gather(*tasks, return_exceptions=True)
    final_points = []
    for res in results_per_post:
        if isinstance(res, Exception):
            print("Error processing a post group:", res)
            continue
        final_points.extend(res)
    return final_points

