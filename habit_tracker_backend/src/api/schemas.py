"""
Pydantic schemas for request/response validation and OpenAPI docs.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date

# ============ AUTH / USER SCHEMAS ============

# PUBLIC_INTERFACE
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="The user's unique email address")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password for the user account")

class UserResponse(UserBase):
    id: int = Field(..., description="Unique user ID")
    created_at: datetime

    class Config:
        orm_mode = True

# PUBLIC_INTERFACE
class Token(BaseModel):
    access_token: str
    token_type: str

# ============ HABIT SCHEMAS ============

class HabitBase(BaseModel):
    title: str = Field(..., description="Title of the habit")
    category: Optional[str] = Field(None, description="Category, e.g., Health/Work/Other")
    reminder_time: Optional[str] = Field(None, description="Reminder time in HH:MM format")

class HabitCreate(HabitBase):
    pass

class HabitUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    reminder_time: Optional[str] = None

class HabitResponse(HabitBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

# ============ COMPLETION SCHEMAS ============

class CompletionBase(BaseModel):
    habit_id: int
    completed_date: date = Field(..., description="The date when habit was completed (YYYY-MM-DD)")

class CompletionCreate(CompletionBase):
    pass

class CompletionResponse(CompletionBase):
    id: int
    user_id: int
    completed_at: datetime

    class Config:
        orm_mode = True

# ============ ANALYTICS SCHEMAS ============

class AnalyticsByCategoryResponse(BaseModel):
    category: str
    completed_count: int

class AnalyticsByDateResponse(BaseModel):
    date: date
    completed_count: int

# ============ COMMON ============

class Message(BaseModel):
    message: str
