from sqlalchemy import create_engine, text
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  relationship, sessionmaker




def create_database_if_not_exists(user, password, host, dbname):
    """Checks if database exists and creates one if it does not"""
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}/postgres")

    with engine.connect() as conn:
        # Check if Database exists
        result = conn.execute(text(f"SELECT 1 from pg_database WHERE datname='{dbname}'"))

        if not result.scalar(): # No rows returned means the DB doesn't exist
            conn.execute(text("COMMIT")) # PostgreSQL requires a Commit before creating a db
            conn.execute(text(f"CREATE DATABASE {dbname}"))
            print(f"Database {dbname} created successfully")
        else:
            print(f"Database {dbname} already exists")

def create_tables(user, password, host, dbname):
    Base = declarative_base()

    class ticker(Base):
        __tablename__ = "tickers"
        id = Column(Integer, primary_key=True)
        symbol = Column(String(10), unique=True, nullable=False)
        name = Column(String(100))
        overall_sentiment_score = Column(
            Integer,
            CheckConstraint("overall_sentiment_score BETWEEN 1 and 100"),
            nullable=True
        )
        last_analyzed = Column(DateTime)

    # Relationships
    posts = relationship("Post", back_populates="ticker", cascade="all, delete-orphan")
    points = relationship("Point", back_populates="ticker", cascade="all, delete-orphan")

def __repr__(self):
    return f"<Ticker(id{self.id}, symbol{self.symbol}', name='{self.name}')>"