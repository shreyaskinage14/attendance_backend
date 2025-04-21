from fastapi import FastAPI
from app.core.database import Base, engine
from app.api.v1.routes import user, attendance

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(attendance.router, prefix="/api/v1/attendance", tags=["Attendance"])
