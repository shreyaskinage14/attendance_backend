from sqlalchemy.orm import Session
from app.models.leave_request import LeaveRequest, LeaveStatus
from app.schemas.leave_request import LeaveRequestCreate, LeaveStatusUpdate
from sqlalchemy import func, extract
from datetime import datetime

def apply_leave(db: Session, user_id: int, leave: LeaveRequestCreate):
    db_leave = LeaveRequest(
        user_id=user_id,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        status=LeaveStatus.pending
    )
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave

def get_user_leaves(db: Session, user_id: int):
    return db.query(LeaveRequest).filter(LeaveRequest.user_id == user_id).all()

def update_leave_status(db: Session, leave_id: int, status_update: LeaveStatusUpdate):
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave:
        return None
    leave.status = status_update.status
    db.commit()
    db.refresh(leave)
    return leave


def get_leave_summary(db: Session, user_id: int):
    now = datetime.now()
    current_month = now.month
    current_year = now.year

    # Count Approved Leaves (Current Year)
    total_approved_year = db.query(func.count()).filter(
        LeaveRequest.user_id == user_id,
        extract('year', LeaveRequest.start_date) == current_year,
        LeaveRequest.status == LeaveStatus.approved
    ).scalar()

    # Count Approved (Current Month)
    total_approved_month = db.query(func.count()).filter(
        LeaveRequest.user_id == user_id,
        extract('month', LeaveRequest.start_date) == current_month,
        extract('year', LeaveRequest.start_date) == current_year,
        LeaveRequest.status == LeaveStatus.approved
    ).scalar()

    # Count Pending (Current Month)
    total_pending_month = db.query(func.count()).filter(
        LeaveRequest.user_id == user_id,
        extract('month', LeaveRequest.start_date) == current_month,
        extract('year', LeaveRequest.start_date) == current_year,
        LeaveRequest.status == LeaveStatus.pending
    ).scalar()

    # Count Rejected (Current Month)
    total_rejected_month = db.query(func.count()).filter(
        LeaveRequest.user_id == user_id,
        extract('month', LeaveRequest.start_date) == current_month,
        extract('year', LeaveRequest.start_date) == current_year,
        LeaveRequest.status == LeaveStatus.rejected
    ).scalar()

    allowed_leaves = 20  # Per year
    leave_balance = allowed_leaves - total_approved_year

    return {
        "approved_leaves": total_approved_month,
        "pending_leaves": total_pending_month,
        "rejected_leaves": total_rejected_month,
        "leave_balance": leave_balance
    }