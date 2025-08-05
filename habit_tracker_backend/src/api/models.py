"""
SQLAlchemy models for the Habit Tracker backend.
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

# PUBLIC_INTERFACE
class User(Base):
    """User table. Holds authentication and profile info."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    habits = relationship("Habit", back_populates="owner", cascade="all, delete-orphan")
    completions = relationship("Completion", back_populates="user", cascade="all, delete-orphan")

# PUBLIC_INTERFACE
class Habit(Base):
    """Represents a habit tracked by a user."""
    __tablename__ = 'habits'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=True)
    reminder_time = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="habits")
    completions = relationship("Completion", back_populates="habit", cascade="all, delete-orphan")

# PUBLIC_INTERFACE
class Completion(Base):
    """Represents a completed habit record (per date)."""
    __tablename__ = 'completions'

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    completed_date = Column(Date, nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
    
    habit = relationship("Habit", back_populates="completions")
    user = relationship("User", back_populates="completions")
