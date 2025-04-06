from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models.stock_index import Base
from config.database_url import STOCKS_DATABASE_URL
from contextlib import contextmanager

# Create the Engine and session factory
engine = create_engine(STOCKS_DATABASE_URL, pool_pre_ping=True)
StockIndexSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Tables if they don't exist
Base.metadata.create_all(bind=engine)

@contextmanager
def stockindex_session_scope():
    session = StockIndexSessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
