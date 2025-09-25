from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.class_group import ClassGroup
from app.schemas.class_group import ClassGroupCreate, ClassGroupOut
from app.dependencies.auth import AdminOnly, TeacherOnly, AnyUser


router = APIRouter(prefix="/class-groups", tags=["class_groups"])


@router.post("/", response_model=ClassGroupOut)
def create_class_group(payload: ClassGroupCreate, db: Session = Depends(get_db), _=Depends(AdminOnly)):
    if db.query(ClassGroup).filter(ClassGroup.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Class group already exists")
    cg = ClassGroup(**payload.model_dump())
    db.add(cg)
    db.commit()
    db.refresh(cg)
    return cg


@router.get("/", response_model=list[ClassGroupOut])
def list_class_groups(db: Session = Depends(get_db), _=Depends(AnyUser)):
    return db.query(ClassGroup).all()


@router.patch("/{group_id}", response_model=ClassGroupOut)
def update_class_group(group_id: int, payload: ClassGroupCreate, db: Session = Depends(get_db), _=Depends(AdminOnly)):
    cg = db.get(ClassGroup, group_id)
    if not cg:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in payload.model_dump().items():
        setattr(cg, k, v)
    db.commit()
    db.refresh(cg)
    return cg


@router.delete("/{group_id}")
def delete_class_group(group_id: int, db: Session = Depends(get_db), _=Depends(AdminOnly)):
    cg = db.get(ClassGroup, group_id)
    if not cg:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(cg)
    db.commit()
    return {"detail": "deleted"}