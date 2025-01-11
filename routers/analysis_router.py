from fastapi import APIRouter, Query
from pydantic import BaseModel
from routers.analysis.check_existing_analysis import check_ticker_in_database
router = APIRouter()

@router.post("/generate-analysis")
def create_analysis(ticker: str, title: str):
    last_analyzed = check_ticker_in_database(ticker)
    
    if last_analyzed is not None:
        return({"message": f"Ticker exists in database and was last analyzed on {last_analyzed}"})
    else:
        return({"message": f"Ticker {ticker} was not yet analyzed"})
