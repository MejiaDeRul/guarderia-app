from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.dependencies.auth import AdminOnly, AnyUser
from app.services.auth import get_password_hash


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def me(current=Depends(AnyUser)):
    return current


@router.post("/", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db), _=Depends(AdminOnly)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    u = User(
        email=payload.email,
        full_name=payload.full_name,
        role=payload.role,
        hashed_password=get_password_hash(payload.password),
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _=Depends(AdminOnly)):
    return db.query(User).all()


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db), _=Depends(AdminOnly)):
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    if payload.full_name is not None:
        u.full_name = payload.full_name
    if payload.role is not None:
        u.role = payload.role
    if payload.password:
        u.hashed_password = get_password_hash(payload.password)
    db.commit()
    db.refresh(u)
    return u


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), _=Depends(AdminOnly)):
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "deleted"}

@router.get("/search", response_model=list[UserOut])
def search_users(
    name: str = Query(..., min_length=2),
    role: UserRole | None = None,
    db: Session = Depends(get_db),
    current=Depends(AnyUser),
):
    q = db.query(User).filter(User.full_name.ilike(f"%{name}%"))

    # Filtro por rol según quién consulta:
    if current.role == UserRole.teacher:
        q = q.filter(User.role == UserRole.parent)          # profe solo ve padres
    elif current.role == UserRole.parent:
        q = q.filter(User.role == UserRole.teacher)         # padre solo ve profes
    else:
        # admin puede ver cualquiera, o filtrar por 'role' si se pasa
        if role:
            q = q.filter(User.role == role)

    return q.order_by(User.full_name.asc()).limit(10).all()