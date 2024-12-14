from database.db import engine
from database.models.thesisai import Base
from sqlalchemy_utils import database_exists, create_database
from config.database_url import DATABASE_URL, DB_NAME

def create_database_if_not_exists():
    """Checks if database exists and creates one if it does not"""

    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Database {DB_NAME} created successfully")
    
    else:
        print(f"Database {DB_NAME} exists already")
    
def create_tables():
    """Creates tables defined in SQLAlchemy models if they don't already exist"""
    try:
        Base.metadata.create_all(engine)
        print("All Tables created successfully (if not already present)")
    except Exception as e:
        print(f"Error creating tables: {e}")    


if __name__ == "__main__":
    # Create Database if it doesn't exist
    create_database_if_not_exists()

    # Create Tables
    create_tables()
    
