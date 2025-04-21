from pydantic import BaseModel
from datetime import datetime

class AttendanceOut(BaseModel):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
