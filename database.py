import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.environment import db_URI

logger = logging.getLogger(__name__)

database_url = db_URI

if not database_url:
    logger.warning("DATABASE_URL not set in .env file. Using SQLite fallback database.")
    database_url = "sqlite:///./productivity.db"

try:
    if database_url.startswith("sqlite"):
        engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False}
        )
    else:
        engine = create_engine(database_url)
    
    display_url = database_url.split('@')[-1] if '@' in database_url else database_url
    logger.info(f"Database engine created successfully: {display_url}")
except Exception as error:
    logger.error(f"Failed to create database engine: {str(error)}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()
