from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from sqlalchemy import desc, func
from datetime import datetime, time

def mark_attendance(db: Session, user_id: int):
    # Find the last attendance record
    last_record = db.query(Attendance).filter(Attendance.user_id == user_id).order_by(desc(Attendance.check_in)).first()

    if last_record and last_record.check_out is None:
        # If last record has no check_out → mark checkout time
        last_record.check_out = func.now()
        db.commit()
        db.refresh(last_record)
        return last_record
    else:
        # Else create a new check-in record
        new_record = Attendance(user_id=user_id)
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return new_record

def get_attendance(db: Session, user_id: int):
    return db.query(Attendance).filter(Attendance.user_id == user_id).order_by(desc(Attendance.check_in)).all()

def get_today_attendance(db: Session, user_id: int):
    today = datetime.now().date()

    start_datetime = datetime.combine(today, time.min)  # 00:00:00
    end_datetime = datetime.combine(today, time.max)    # 23:59:59

    return db.query(Attendance).filter(
        Attendance.user_id == user_id,
        Attendance.check_in >= start_datetime,
        Attendance.check_in <= end_datetime
    ).all()
