from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud.attendance import mark_attendance, get_attendance
from app.schemas.attendance import AttendanceOut
from app.utils.auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/mark", response_model=AttendanceOut)
def mark(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return mark_attendance(db, current_user)

@router.get("/history", response_model=list[AttendanceOut])
def history(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return get_attendance(db, current_user)
