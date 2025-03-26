from database.models.thesisai import Base
from database.db import engine
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

def create_vector_extension():
    with engine.connect() as conn:
        try:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        except Exception as e:
            print(f"Could not create vector extension: {e}")
        conn.commit()

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
    # Create Database if it doesn't exist
    print("CREATING DATABASE")
    create_database_if_not_exists()
    print("CREATING VECTOR EXTENSION")
    create_vector_extension()
    print("CREATING TABLES")
    # Create Tables
    create_tables()
    
