"""
DB integration for the Habit Tracker backend.

This handles the SQLAlchemy engine/session, Base class, 
and table creation.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PUBLIC_INTERFACE
def get_database_url():
    """Read DB URL from environment variable (should be in .env)."""
    import os
    return os.environ.get("DATABASE_URL", "sqlite:///./habit_tracker.db")

DATABASE_URL = get_database_url()
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# PUBLIC_INTERFACE
def get_db():
    """Yield a DB session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
