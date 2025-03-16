import requests as r
import json
import os
from dotenv import load_dotenv

ENV_PATH = os.getenv("ENV_PATH")
load_dotenv(ENV_PATH)
api_key = os.getenv("FMP_API_KEY")

BASE_URL = "https://financialmodelingprep.com/api/v3/"

def response_to_json(data):
    try:
        json_response = data.json()
        # Check if the response is a list before trying to access index 0
        if isinstance(json_response, list) and len(json_response) > 0:
            json_data = json_response[0] # The api should returns a list of dictionaries
        else:
            json_data = json_response
    except (IndexError, ValueError):
        json_data = {}
    
    return json_data


def get_stock_profile(ticker):
    
    profile_response = r.get(
        url=f"{BASE_URL}profile/{ticker}",
        params = {
            "apikey": api_key
        }
    )
    profile_data = response_to_json(profile_response)
    
    
    stock_info = {
        "symbol": profile_data.get("symbol", "N/A"),
        "companyName": profile_data.get("companyName", "N/A"),
        "image": profile_data.get("image", "N/A") if r.get(profile_data.get("image")).status_code == 200 else None, # This is a link to an image that gets returned even when there is no image. In that case the link that's returned will just point to a 404
        "website": profile_data.get("website", "N/A"),
        "description": profile_data.get("description", "N/A"),
        "price": profile_data.get("price", "N/A"),
        "exchangeShortName": profile_data.get("exchangeShortName", "N/A"),
        "mktCap": profile_data.get("mktCap", "N/A"),
        "industry": profile_data.get("industry", "N/A"),
        "dcf": profile_data.get("dcf", "N/A"),
        "beta": profile_data.get("beta", "N/A"),
    }

    return stock_info


if __name__ == "__main__":
    ticker = input("Ticker: ")
    profile = get_stock_profile(ticker)

    print(json.dumps(profile, indent=4))
