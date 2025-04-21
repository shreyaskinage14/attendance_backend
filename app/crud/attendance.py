from sqlalchemy.orm import Session
from app.models.attendance import Attendance

def mark_attendance(db: Session, user_id: int):
    record = Attendance(user_id=user_id)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_attendance(db: Session, user_id: int):
    return db.query(Attendance).filter(Attendance.user_id == user_id).all()
