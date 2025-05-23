from fastapi import APIRouter
from .analysis.check_existing_analysis import check_ticker_in_database

router = APIRouter()

@router.get("/check-analysis")
def create_analysis(ticker: str):
    ticker_exists, last_analyzed = check_ticker_in_database(ticker)
    
    if ticker_exists:
        if last_analyzed is not None:
            return {
                "existing_analysis": True,
                "message": f"There is an existing analysis for '{ticker}' created on {last_analyzed}. Do you want to access it or create a new analysis?"
            }
        else:
            return {
                "existing_analysis": True,
                "message": f"'{ticker}' exists in the database, but no analysis has been done yet."
            }
    else:
        return {
            "existing_analysis": False,
            "message": f"{ticker} was not found in the database. Do you want to generate a new analysis for it?"
        }
