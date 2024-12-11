from fastapi import APIRouter, Query
from sqlalchemy import  select, create_engine, func, case, text
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
def search_stock(q: str = Query(..., min_length=1), r: str = Query(...)):
    # Limit Number of results to keep it responsive
    limit = 10
    with Session() as session:
        # use ILIKE with indexes
        if r == "relevance":
            print("relevance activated")
            stmt = select(
                stocks_table.c.ticker,
                stocks_table.c.title,
                func.similarity(stocks_table.c.title, q).label("relevance")
                ).where((stocks_table.c.ticker.ilike(f"%{q}%")) | 
                        (stocks_table.c.title.ilike(f"%{q}%"))
                ).order_by(func.similarity(stocks_table.c.title, q).desc())\
                .limit(limit)
            results = session.execute(stmt).all()
        elif r == "default":
            print("relevance deactivated")
            stmt = select(stocks_table.c.ticker, stocks_table.c.title)\
            .where((stocks_table.c.ticker.ilike(f"%{q}%")) | (stocks_table.c.title.ilike(f"%{q}%")))\
            .limit(limit)
            results = session.execute(stmt).all()
        elif r == "case":
            print("case activated")
            stmt = select(
                stocks_table.c.ticker,
                stocks_table.c.title,
                case(
                    # Exact ticker match gets highest priority
                    (stocks_table.c.ticker.ilike(q), 1),
                    # Partial ticker match gets medium priority
                    else_=2
                ).label("priority")
            ).where(
                (stocks_table.c.ticker.ilike(f"%{q}%")) | 
                (stocks_table.c.title.ilike(f"%{q}%"))
                
            ).order_by("priority", stocks_table.c.title.asc())\
            .limit(limit)
            
            results = session.execute(stmt).all()

        elif r == "combined":
            stmt = select(
                stocks_table.c.ticker,
                stocks_table.c.title,
                # Calculate weighted relevance score
                (
                    case((stocks_table.c.ticker.ilike(q), 1.0), else_=0.0) + # Exact ticker match
                    func.similarity(stocks_table.c.ticker, q) * 0.8 +        # Partial ticker match
                    func.similarity(stocks_table.c.title, q) * 0.2           # partial title match
                ).label("relevance")
            ).where(
                stocks_table.c.ticker.ilike(f"%{q}%") | stocks_table.c.title.ilike(f"%{q}%")
            ).order_by(text("relevance DESC"))\
            .limit(limit)

            results = session.execute(stmt).all()

    return [{"ticker":  r[0], "title": r[1]} for r in results]