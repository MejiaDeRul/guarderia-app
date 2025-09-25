from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.child import Child
from app.schemas.child import ChildCreate, ChildOut
from app.dependencies.auth import AdminOnly, ParentOnly, TeacherOnly, AnyUser


router = APIRouter(prefix="/children", tags=["children"])


@router.post("/", response_model=ChildOut)
def create_child(payload: ChildCreate, db: Session = Depends(get_db), _=Depends(AdminOnly)):
    c = Child(**payload.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.get("/", response_model=list[ChildOut])
def list_children(db: Session = Depends(get_db), _=Depends(TeacherOnly)):
    return db.query(Child).all()


@router.get("/mine", response_model=list[ChildOut])
def my_children(current=Depends(ParentOnly)):
    return current.children


@router.delete("/{child_id}")
def delete_child(child_id: int, db: Session = Depends(get_db), _=Depends(AdminOnly)):
    c = db.get(Child, child_id)
    if not c:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(c)
    db.commit()
    return {"detail": "deleted"}