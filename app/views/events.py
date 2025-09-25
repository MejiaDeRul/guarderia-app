from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.session import get_db
from app.models.event import Event
from app.schemas.event import EventCreate, EventOut, EventUpdate
from app.dependencies.auth import AdminOnly, TeacherOnly, ParentOnly, AnyUser


router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventOut)
def create_event(payload: EventCreate, db: Session = Depends(get_db), _=Depends(TeacherOnly)):
    if payload.end_at <= payload.start_at:
        raise HTTPException(status_code=400, detail="end_at must be after start_at")
    ev = Event(**payload.model_dump())
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


@router.get("/", response_model=list[EventOut])
def list_events(db: Session = Depends(get_db), _=Depends(AnyUser)):
    return db.query(Event).all()


@router.get("/by-class/{group_id}", response_model=list[EventOut])
def list_by_class(group_id: int, db: Session = Depends(get_db), _=Depends(AnyUser)):
    return db.query(Event).filter(Event.class_group_id == group_id).all()


@router.get("/by-child/{child_id}", response_model=list[EventOut])
def list_by_child(child_id: int, db: Session = Depends(get_db), _=Depends(AnyUser)):
    return db.query(Event).filter(Event.child_id == child_id).all()


@router.patch("/{event_id}", response_model=EventOut)
def update_event(event_id: int, payload: EventUpdate, db: Session = Depends(get_db), _=Depends(TeacherOnly)):
    ev = db.get(Event, event_id)
    if not ev:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(ev, k, v)
    db.commit()
    db.refresh(ev)
    return ev


@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db), _=Depends(TeacherOnly)):
    ev = db.get(Event, event_id)
    if not ev:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(ev)
    db.commit()
    return {"detail": "deleted"}