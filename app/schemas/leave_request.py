from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum

class LeaveStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class LeaveRequestCreate(BaseModel):
    start_date: date
    end_date: date
    reason: str

class LeaveRequestOut(BaseModel):
    id: int
    start_date: date
    end_date: date
    reason: str
    status: LeaveStatus

    class Config:
        from_attributes = True

class LeaveStatusUpdate(BaseModel):
    status: LeaveStatus

class LeaveSummaryOut(BaseModel):
    approved_leaves: int
    pending_leaves: int
    rejected_leaves: int
    leave_balance: int
