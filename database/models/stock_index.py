from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

stocks_table = Table(
    "stocks", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("ticker", String, index=True),
    Column("title", String)
)
