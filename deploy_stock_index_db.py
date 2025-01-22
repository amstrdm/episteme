from database.db import engine
from sqlalchemy import text, Index
from sqlalchemy.dialects.postgresql import insert
import os
from sqlalchemy_utils import database_exists, create_database
import json
from database.models.stock_index import metadata, stocks_table
from config.database_url import STOCKS_DATABASE_URL, STOCKS_DB_NAME

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DATA_PATH = os.path.join(BASE_DIR, "./data/sec_tickers.json")
print(STOCKS_DATABASE_URL)
print(STOCKS_DB_NAME)
# Define trigram indexes
idx_ticker_trgm = Index(
    "idx_stocks_ticker_trgm",
    stocks_table.c.ticker,
    postgresql_using="gin",
    postgresql_ops={"ticker": "gin_trgm_ops"}
)

idx_title_trgm = Index(
    "idx_stocks_title_trgm",
    stocks_table.c.title,
    postgresql_using="gin",
    postgresql_ops={"title": "gin_trgm_ops"}
)



# Check if database exists and create one if it does not

if not database_exists(engine.url):
    create_database(engine.url)
    print(f"Database {STOCKS_DB_NAME} created successfully")

else:
    print(f"Database {STOCKS_DB_NAME} exists already")

# Enable the pg_trgm extension (must be done before creating trigram indexes)
with engine.connect() as conn:
    try:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
    except Exception as e:
        print(f"Could not create pg_trgm extension: {e}")
    conn.commit()

# Create tables if they don't already exist
try:
    metadata.create_all(engine)
    print("All Tables created successfully (if not already present)")
except Exception as e:
    print(f"Error creating tables: {e}")    

# Read JSON data
try:
    with open(JSON_DATA_PATH, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"JSON data file not found. Please place a JSON file containing stock tickers and names into {JSON_DATA_PATH}")

records = list(data.values())

# Insert Data into the table
with engine.connect() as conn:
    try:
        conn.execute(text("TRUNCATE stocks;")) # We clear all existing data
    except Exception as e:
        print(f"Could not truncate table: {e}")
    
    try:
        conn.execute(insert(stocks_table), records)
    except Exception as e:
        print(f"Could not insert data into table: {e}")
    conn.commit()

print("Stock Index Database Setup complete and data insertion complete!")