from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud.attendance import mark_attendance, get_attendance
from app.schemas.attendance import AttendanceOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/mark", response_model=AttendanceOut)
def mark(user_id: int, db: Session = Depends(get_db)):
    return mark_attendance(db, user_id)

@router.get("/history", response_model=list[AttendanceOut])
def history(user_id: int, db: Session = Depends(get_db)):
    return get_attendance(db, user_id)
