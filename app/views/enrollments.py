from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.enrollment import Enrollment
from app.models.child import Child
from app.models.class_group import ClassGroup
from app.schemas.enrollment import EnrollmentCreate, EnrollmentOut
from app.dependencies.auth import AdminOnly, TeacherOnly


router = APIRouter(prefix="/enrollments", tags=["enrollments"])


@router.post("/", response_model=EnrollmentOut)
def enroll(payload: EnrollmentCreate, db: Session = Depends(get_db), _=Depends(AdminOnly)):
    child = db.get(Child, payload.child_id)
    group = db.get(ClassGroup, payload.class_group_id)
    if not child or not group:
        raise HTTPException(status_code=400, detail="Invalid child or group")
    e = Enrollment(**payload.model_dump())
    db.add(e)
    db.commit()
    db.refresh(e)
    return e


@router.get("/by-class/{group_id}", response_model=list[EnrollmentOut])
def by_class(group_id: int, db: Session = Depends(get_db), _=Depends(TeacherOnly)):
    return db.query(Enrollment).filter(Enrollment.class_group_id == group_id).all()