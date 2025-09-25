from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.message import Message
from app.models.user import UserRole
from app.schemas.message import MessageCreate, MessageOut
from app.dependencies.auth import AnyUser


router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageOut)
def send_message(payload: MessageCreate, current=Depends(AnyUser), db: Session = Depends(get_db)):
# Restrict: only teacher <-> parent chats
    if current.role not in (UserRole.teacher, UserRole.parent):
        raise HTTPException(status_code=403, detail="Only teacher/parent can message")
    msg = Message(sender_id=current.id, **payload.model_dump())
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


@router.get("/with/{user_id}", response_model=list[MessageOut])
def conversation_with(user_id: int, current=Depends(AnyUser), db: Session = Depends(get_db)):
    q = db.query(Message).filter(
        ((Message.sender_id == current.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current.id))
    ).order_by(Message.sent_at.asc())
    return q.all()