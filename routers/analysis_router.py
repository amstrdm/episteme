from fastapi import APIRouter, Query
from pydantic import BaseModel
from routers.analysis.check_existing_analysis import check_ticker_in_database
router = APIRouter()

class StockQuery(BaseModel):
    ticker: str
    title: str
    online_confirmed: bool = False # Checking if User wants to access offline analysis

@router.post("/generate-analysis")
def create_analysis(stock: StockQuery):
    last_analyzed = check_ticker_in_database(stock.ticker)
    if last_analyzed is not None:
        return({"message": f"Ticker exists in database and was last analyzed on {last_analyzed}"})
    else:
        return({"message": f"Ticker {stock.ticker} was not yet analyzed"})