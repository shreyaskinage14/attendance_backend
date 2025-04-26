from pydantic import BaseModel
from datetime import datetime

class AttendanceOut(BaseModel):
    id: int
    check_in: datetime
    check_out: datetime | None  # 👈 Optional, because user may not have logged out yet

    class Config:
        from_attributes = True
