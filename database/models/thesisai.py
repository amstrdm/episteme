from sqlalchemy import Text, Column, Integer, String, DateTime, Boolean, ForeignKey, CheckConstraint, Float
from sqlalchemy.orm import  relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY

Base = declarative_base()

class Ticker(Base):
    __tablename__ = "tickers"
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), unique=True, nullable=False)
    name = Column(String(100))
    description = Column(Text)
    overall_sentiment_score = Column(
        Integer,
        CheckConstraint("overall_sentiment_score BETWEEN 1 and 100"),
        nullable=True
    )
    last_analyzed = Column(DateTime)
    description_last_analyzed = Column(DateTime)

    # Relationships
    posts = relationship("Post", back_populates="ticker", cascade="all, delete-orphan")
    points = relationship("Point", back_populates="ticker", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Ticker(id{self.id}, symbol{self.symbol}', name='{self.name}')>"

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    ticker_id = Column(ForeignKey("tickers.id"), nullable=False)
    source = Column(String(50), nullable=False)
    title = Column(String(250))
    link = Column(Text)
    date_of_post = Column(DateTime)
    content = Column(Text)

    # Relationships 

    ticker = relationship("Ticker", back_populates="posts")
    points = relationship("Point", back_populates="post", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Post(id{self.id}, source='{self.source}', title='{self.title}')>"
    
class Point(Base):
    __tablename__ = "points"
    id = Column(Integer, primary_key=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), nullable=False)
    post_id = Column(ForeignKey("posts.id"), nullable=False)
    sentiment_score = Column(
        Integer,
        CheckConstraint("sentiment_score BETWEEN 1 and 100"),
        nullable=False
    )
    text = Column(Text, nullable=False)
    criticism_exists = Column(Boolean, default=False)
    embedding = Column(ARRAY(Float))
    
    # Relationships
    ticker = relationship("Ticker", back_populates="points")
    post = relationship("Post", back_populates="points")
    criticisms = relationship("Criticism", back_populates="point", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Point(id={self.id}, sentiment_score={self.sentiment_score}, text='{self.text[:30]}...')>"
        
class Criticism(Base):
    __tablename__ = "criticisms"
    id = Column(Integer, primary_key=True)
    point_id = Column(Integer, ForeignKey("points.id"), nullable=False)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    text = Column(Text, nullable=False)
    date_posted = Column(DateTime)
    validity_score = Column(
        Integer,
        CheckConstraint("validity_score BETWEEN 1 and 100"),
        nullable=True           
    )

    # Relationships 

    point = relationship("Point", back_populates="criticisms")
    comment = relationship("Comment", back_populates="criticisms")
    def __repr__(self):
        return f"<Criticism(id={self.id}, valdiity_score={self.validity_score})>"

class Comment(Base):
    __tablename_ = "comments"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=True)
    
    # Relationships

    post = relationship("Post", back_populates="comments")
    criticisms = relationship("Criticism", back_populates="comment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Comment(id={self.id}, post_id={self.post_id}, author='{self.author}', date_posted={self.date_posted})>"

