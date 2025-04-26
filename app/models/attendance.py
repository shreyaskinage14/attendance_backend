from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, DateTime, ForeignKey, func
from app.core.database import Base
from datetime import datetime

class Attendance(Base):
    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    check_in: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    check_out: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
