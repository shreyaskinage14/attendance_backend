from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.leave_request import LeaveRequestCreate, LeaveRequestOut, LeaveStatusUpdate
from app.crud.leave_request import apply_leave, get_user_leaves, update_leave_status, get_leave_summary
from app.core.database import SessionLocal
from app.utils.auth import get_current_user
from app.schemas.leave_request import LeaveSummaryOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/apply", response_model=LeaveRequestOut)
def apply_leave_api(leave: LeaveRequestCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return apply_leave(db, current_user, leave)

@router.get("/history", response_model=list[LeaveRequestOut])
def leave_history_api(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return get_user_leaves(db, current_user)

@router.put("/update/{leave_id}", response_model=LeaveRequestOut)
def update_leave_status_api(leave_id: int, status: LeaveStatusUpdate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    leave = update_leave_status(db, leave_id, status)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    return leave

@router.get("/summary", response_model=LeaveSummaryOut)
def leave_summary_api(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return get_leave_summary(db, current_user)
