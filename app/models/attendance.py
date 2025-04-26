from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from app.core.database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    check_in = Column(DateTime(timezone=True), server_default=func.now())
    check_out = Column(DateTime(timezone=True), nullable=True)  # 👈 New field
