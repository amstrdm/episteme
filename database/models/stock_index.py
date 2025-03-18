from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

metadata = MetaData()

stocks_table = Table(
    "stocks", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("ticker", String, index=True),
    Column("title", String)
)
