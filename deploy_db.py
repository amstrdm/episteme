from sqlalchemy import create_engine
from database.models.thesisai import Base
from dotenv import load_dotenv
import os
from sqlalchemy_utils import database_exists, create_database

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "./config/config.env")

load_dotenv(ENV_PATH)

def create_database_if_not_exists(user, password, host, dbname):
    """Checks if database exists and creates one if it does not"""
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}/{dbname}")

    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Database {dbname} created successfully")
    
    else:
        print(f"Database {dbname} exists already")
    
def create_tables(user, password, host, dbname):
    """Creates tables defined in SQLAlchemy models if they don't already exist"""
    db_url = f"postgresql+psycopg2://{user}:{password}@{host}/{dbname}"
    engine = create_engine(db_url)

    try:
        Base.metadata.create_all(engine)
        print("All Tables created successfully (if not already present)")
    except Exception as e:
        print(f"Error creating tables: {e}")    


if __name__ == "__main__":
    DB_USER = os.getenv("POSTGRESQL_USER")
    DB_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
    DB_HOST = os.getenv("POSTGRESQL_HOST")
    DB_NAME = os.getenv("POSTGRESQL_DBNAME")

    # Create Database if it doesn't exist
    create_database_if_not_exists(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

    # Create Tables
    create_tables(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
    
