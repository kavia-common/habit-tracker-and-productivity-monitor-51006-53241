"""
CRUD and completion endpoints for habits, protected by authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from . import schemas, models
from .database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/habits", tags=["Habits"])

# ========== CREATE HABIT ==========

# PUBLIC_INTERFACE
@router.post("/", response_model=schemas.HabitResponse)
def create_habit(habit_in: schemas.HabitCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Create a new habit for the authenticated user.
    """
    habit = models.Habit(**habit_in.dict(), owner_id=user.id)
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit

# ========== READ ALL HABITS ==========

# PUBLIC_INTERFACE
@router.get("/", response_model=List[schemas.HabitResponse])
def get_habits(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Get all habits for the authenticated user.
    """
    return db.query(models.Habit).filter(models.Habit.owner_id == user.id).all()

# ========== READ SINGLE HABIT ==========

# PUBLIC_INTERFACE
@router.get("/{habit_id}", response_model=schemas.HabitResponse)
def get_habit(habit_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Get details of a habit.
    """
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id, models.Habit.owner_id == user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

# ========== UPDATE HABIT ==========

# PUBLIC_INTERFACE
@router.put("/{habit_id}", response_model=schemas.HabitResponse)
def update_habit(habit_id: int, habit_update: schemas.HabitUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Update a habit.
    """
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id, models.Habit.owner_id == user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    for k, v in habit_update.model_dump(exclude_unset=True).items():
        setattr(habit, k, v)
    db.commit()
    db.refresh(habit)
    return habit

# ========== DELETE HABIT ==========

# PUBLIC_INTERFACE
@router.delete("/{habit_id}", response_model=schemas.Message)
def delete_habit(habit_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Delete a habit (and its completions).
    """
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id, models.Habit.owner_id == user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    db.delete(habit)
    db.commit()
    return {"message": "Habit deleted"}

# ========== MARK HABIT AS COMPLETE ==========

# PUBLIC_INTERFACE
@router.post("/{habit_id}/complete", response_model=schemas.CompletionResponse)
def complete_habit(habit_id: int, completed_date: date = Query(None, description="Date to mark as complete (default: today)"), db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Mark a habit as complete for a given date (default today).
    """
    if completed_date is None:
        completed_date = date.today()
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id, models.Habit.owner_id == user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    exists = db.query(models.Completion).filter(
        models.Completion.habit_id == habit_id,
        models.Completion.user_id == user.id,
        models.Completion.completed_date == completed_date
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Habit already marked complete for this date")
    completion = models.Completion(
        habit_id=habit_id,
        user_id=user.id,
        completed_date=completed_date
    )
    db.add(completion)
    db.commit()
    db.refresh(completion)
    return completion

# ========== GET COMPLETIONS BY USER ==========

# PUBLIC_INTERFACE
@router.get("/completions", response_model=List[schemas.CompletionResponse])
def get_completions(habit_id: Optional[int] = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    List completion records for user (optionally filtered by habit).
    """
    query = db.query(models.Completion).filter(models.Completion.user_id == user.id)
    if habit_id:
        query = query.filter(models.Completion.habit_id == habit_id)
    return query.order_by(models.Completion.completed_date.desc()).all()
