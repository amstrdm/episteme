from sqlalchemy import create_engine, Text, Column, Integer, Table, String, MetaData, text, Index
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
import json
from database.models.stock_index import stocks_table

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "./config/config.env")
JSON_DATA_PATH = os.path.join(BASE_DIR, "./data/sec_tickers.json")

load_dotenv(ENV_PATH)
DB_USER = os.getenv("POSTGRESQL_USER")
DB_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
DB_HOST = os.getenv("POSTGRESQL_HOST")
DB_NAME = os.getenv("POSTGRESQL_STOCKS_DBNAME")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
metadata = MetaData()

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
    print(f"Database {DB_NAME} created successfully")

else:
    print(f"Database {DB_NAME} exists already")

# Enable the pg_trgm extension (must be done before creating trigram indexes)
with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
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
    conn.execute(text("TRUNCATE stocks;")) # We clear all existing data
    conn.execute(insert(stocks_table), records)
    conn.commit()

print("Stock Index Database Setup complete and data insertion complete!")