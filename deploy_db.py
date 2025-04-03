from database.models.thesisai import Base
from sqlalchemy_utils import database_exists, create_database
from config.database_url import DATABASE_URL, DB_NAME
from sqlalchemy import text

def create_database_if_not_exists():
    """Checks if database exists and creates one if it does not"""
    try:
        if not database_exists(DATABASE_URL):
            create_database(DATABASE_URL)
            print(f"Database {DB_NAME} created successfully\n")
        else:
            print(f"Database {DB_NAME} exists already\n")
    except Exception as e:
        print ("Error Creating Database:", e)

def create_tables():
    """Creates tables defined in SQLAlchemy models if they don't already exist"""
    try:
        from database.db import engine
    except Exception as e:
        print("Error importing engine. Are you sure the database was created?:", e)
    
    try:
        Base.metadata.create_all(engine)
        print("All Tables created successfully (if not already present)\n")
    except Exception as e:
        print(f"Error creating tables: {e}")


if __name__ == "__main__":
    print(f"DATABASE_URL: {DATABASE_URL}")
    print(f"DB_NAME: {DB_NAME}\n")

    # Create Database if it doesn't exist
    print("CREATING DATABASE")
    create_database_if_not_exists()
    print("CREATING TABLES")
    # Create Tables
    create_tables()
    
