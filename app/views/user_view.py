from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.controllers import user_controller
from app.schemas.user_schema import UserCreate, UserRead
from app.dependencies.db import get_db 

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserRead)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(db, user)

@router.get("/", response_model=List[UserRead])
def read_all(db: Session = Depends(get_db)):
    return user_controller.get_users(db)
