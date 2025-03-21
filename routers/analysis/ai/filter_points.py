from typing import Dict
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
from database.models.thesisai import Ticker, Point
from database.db import SessionLocal

ENV_PATH = os.getenv("ENV_PATH")
load_dotenv(ENV_PATH)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("COULD NOT FIND OPENAI API KEY IN summarize_post.py")
client = OpenAI(api_key=OPENAI_API_KEY)


def get_existing_points_as_dict(ticker_obj: Ticker):
    with SessionLocal() as session:
        points = session.query(Point).filter(Point.ticker_id == ticker_obj.id).all()

        points_dict = {
            "thesis_points": [
                {
                    "point": point.text,
                    "sentiment_score": point.sentiment_score
                }
                for point in points
            ]
        }

        return points_dict


def remove_duplicate_points(new_points: Dict, ticker_obj: Ticker):
    existing_points = get_existing_points_as_dict(ticker_obj)

    user_prompt = f"""
    Below are two lists of thesis points. Each thesis point is represented as an object with two fields: "point" (the text) and "sentiment_score" (an integer from 1 to 100).

    List A (New Thesis Points extracted from the latest post):
    {new_points}

    List B (Existing Thesis Points already in the database):
    {existing_points}

    Your task is to filter out any thesis point from List A that is semantically similar to any thesis point in List B. A thesis point is considered semantically similar if it expresses the same core idea, even if the wording is different. Only include in the final output those thesis points from List A that do not match (i.e., are unique compared to) any thesis point in List B.
    """

    response = client.responses.create(
        model="gpt-4o",
        input=[
            {"role": "user", "content": user_prompt}
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "thesis_summarization",
                "schema": {
                    "type": "object",
                    "properties": {
                        "thesis_points": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                            "point": {
                                "type": "string",
                                "description": "The extracted thesis point text."
                            },
                            "sentiment_score": {
                                "type": "integer",
                                "description": "The sentiment score, where 50 is neutral, above 50 is bullish, and below 50 is bearish."
                            }
                            },
                            "required": ["point", "sentiment_score"],
                            "additionalProperties": False
                        }
                        }
                    },
                    "required": ["thesis_points"],
                    "additionalProperties": False
                }
            }
        }
    )

    result_dict = json.loads(response.output_text)
    return result_dict
