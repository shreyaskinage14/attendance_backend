from pydantic import BaseModel

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
