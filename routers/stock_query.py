from fastapi import APIRouter, Query
from sqlalchemy import  select, func, case, text
from dotenv import load_dotenv
import os
from database.models.stock_index import stocks_table
from database.db import SessionLocal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "../config/config.env")

load_dotenv(ENV_PATH)
DB_USER = os.getenv("POSTGRESQL_USER")
DB_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
DB_HOST = os.getenv("POSTGRESQL_HOST")
DB_NAME = os.getenv("POSTGRESQL_STOCKS_DBNAME")

router = APIRouter()

@router.get("/stock-query")
def search_stock(q: str = Query(..., min_length=1)):
    # Limit Number of results to keep it responsive
    limit = 10
    with SessionLocal() as session:
        # use ILIKE with indexes
        stmt = select(
            stocks_table.c.ticker,
            stocks_table.c.title,
            # Calculate weighted relevance score
            (
                case((stocks_table.c.ticker.ilike(q), 1.0), else_=0.0) + # Exact ticker match
                func.similarity(stocks_table.c.ticker, q) * 0.7 +        # Partial ticker match
                func.similarity(stocks_table.c.title, q) * 0.3           # partial title match
            ).label("relevance")
        ).where(
            stocks_table.c.ticker.ilike(f"%{q}%") | stocks_table.c.title.ilike(f"%{q}%")
        ).order_by(text("relevance DESC"))\
        .limit(limit)

        results = session.execute(stmt).all()

    return [{"ticker":  r[0], "title": r[1]} for r in results]