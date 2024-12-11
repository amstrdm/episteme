from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.thesisai import Base
from config.database_url import DATABASE_URL

# Create the Engine and session factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Tables if they don't exist
Base.metadata.create_all(bind=engine)