from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Date, Enum, ForeignKey
from datetime import date  # ✅ Important!
from enum import Enum as PyEnum
from app.core.database import Base

class LeaveStatus(PyEnum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    start_date: Mapped[date] = mapped_column(Date)  # ✅ Correct
    end_date: Mapped[date] = mapped_column(Date)    # ✅ Correct
    reason: Mapped[str] = mapped_column(String)
    status: Mapped[LeaveStatus] = mapped_column(Enum(LeaveStatus), default=LeaveStatus.pending)
