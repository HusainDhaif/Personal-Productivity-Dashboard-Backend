"""
Database setup for the Personal Productivity Dashboard.

This file:
- configures a SQLite database
- creates the SQLAlchemy engine and session
- defines the Base class for our models
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL.
# This will create a file called "productivity.db" in the project directory.
SQLALCHEMY_DATABASE_URL = "sqlite:///./productivity.db"

# The engine is responsible for connecting to the database.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite with FastAPI
)

# SessionLocal will be used to talk to the database (open/close sessions).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that all SQLAlchemy models will inherit from.
Base = declarative_base()


