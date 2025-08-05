"""
Analytics endpoints for completion data by category and by date.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from . import schemas, models
from .database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# PUBLIC_INTERFACE
@router.get("/by-category", response_model=List[schemas.AnalyticsByCategoryResponse])
def completions_by_category(
    from_date: date = Query(None), 
    to_date: date = Query(None), 
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)
):
    """
    Get total completions grouped by habit category for the user.
    """
    query = db.query(
        models.Habit.category,
        db.func.count(models.Completion.id).label("completed_count")
    ).join(models.Completion, models.Completion.habit_id == models.Habit.id
    ).filter(models.Habit.owner_id == user.id)
    if from_date:
        query = query.filter(models.Completion.completed_date >= from_date)
    if to_date:
        query = query.filter(models.Completion.completed_date <= to_date)
    query = query.group_by(models.Habit.category).all()
    return [schemas.AnalyticsByCategoryResponse(category=row.category or "(Uncategorized)", completed_count=row.completed_count) for row in query]

# PUBLIC_INTERFACE
@router.get("/by-date", response_model=List[schemas.AnalyticsByDateResponse])
def completions_by_date(
    habit_id: int = Query(None), 
    from_date: date = Query(None), 
    to_date: date = Query(None), 
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)
):
    """
    Get total completions per day (optionally filter by habit) for user.
    """
    query = db.query(
        models.Completion.completed_date.label("date"),
        db.func.count(models.Completion.id).label("completed_count")
    ).filter(models.Completion.user_id == user.id)
    if habit_id:
        query = query.filter(models.Completion.habit_id == habit_id)
    if from_date:
        query = query.filter(models.Completion.completed_date >= from_date)
    if to_date:
        query = query.filter(models.Completion.completed_date <= to_date)
    query = query.group_by(models.Completion.completed_date).order_by(models.Completion.completed_date).all()
    return [schemas.AnalyticsByDateResponse(date=row.date, completed_count=row.completed_count) for row in query]
