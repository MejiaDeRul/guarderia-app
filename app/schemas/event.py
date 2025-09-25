from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    title: str
    description: str | None = None
    start_at: datetime
    end_at: datetime
    class_group_id: int | None = None
    child_id: int | None = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None


class EventOut(EventBase):
    id: int
    class Config:
        from_attributes = True