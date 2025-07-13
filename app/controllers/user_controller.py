from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate

def create_user(db: Session, user_data: UserCreate):
    user = User(name=user_data.name, email=user_data.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session):
    return db.query(User).all()
