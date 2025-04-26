from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    name: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None