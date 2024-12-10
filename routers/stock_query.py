from fastapi import APIRouter, Query
from sqlalchemy import  select, create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from database.models.stock_index import stocks_table

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "../config/config.env")

load_dotenv(ENV_PATH)
DB_USER = os.getenv("POSTGRESQL_USER")
DB_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
DB_HOST = os.getenv("POSTGRESQL_HOST")
DB_NAME = os.getenv("POSTGRESQL_STOCKS_DBNAME")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
Session = sessionmaker(bind=engine)

router = APIRouter()

@router.get("/stock_query")
def search_stock(q: str = Query(..., min_length=1)):
    # Limit Number of results to keep it responsive
    limit = 10
    with Session() as session:
        # use ILIKE with indexes
        stmt = select(stocks_table.c.ticker, stocks_table.c.title)\
            .where((stocks_table.c.ticker.ilike(f"%{q}%")) | (stocks_table.c.title.ilike(f"%{q}%")))\
            .limit(limit)
        results = session.execute(stmt).all()

    return [{"ticker":  r[0], "title": r[1]} for r in results]