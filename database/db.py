from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models.thesisai import Base
from config.database_url import DATABASE_URL
from contextlib import contextmanager

# Create the Engine and session factory
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Tables if they don't exist
Base.metadata.create_all(bind=engine)

@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
