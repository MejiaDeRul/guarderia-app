from pydantic import BaseModel
from datetime import datetime


class MessageCreate(BaseModel):
    receiver_id: int
    child_id: int | None = None
    content: str


class MessageOut(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    child_id: int | None
    content: str
    sent_at: datetime

    class Config:
        from_attributes = True