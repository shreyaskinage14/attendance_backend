from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, name=user.name, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    db_user.email = user.email
    db_user.name = user.name
    db_user.hashed_password = hash_password(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user
