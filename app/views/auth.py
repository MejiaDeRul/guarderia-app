# app/views/auth.py
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User, UserRole
from app.schemas.common import Token, Msg  # Msg útil para respuestas 4xx/5xx si quieres usarlo
from app.schemas.user import UserCreate, UserOut
from app.services.auth import create_access_token, verify_password, get_password_hash

router = APIRouter(prefix="/auth", tags=["auth"])


# -------- LOGIN --------
@router.post(
    "/login",
    response_model=Token,
    summary="Inicia sesión y obtiene un access token (OAuth2 password)",
    responses={
        401: {"description": "Credenciales incorrectas"},
        422: {"description": "Datos inválidos en el formulario OAuth2"},
    },
)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    """
    Recibe credenciales vía **application/x-www-form-urlencoded**:
    - `username`: email del usuario
    - `password`: contraseña

    Devuelve un **JWT** en `access_token` y `token_type=bearer`.
    """
    user: User | None = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        # 401 controlado, no filtra si el email existe
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # role puede ser Enum; usa .value si aplica
    role_value = getattr(user.role, "value", user.role)
    token = create_access_token(subject=user.email, role=role_value)
    return {"access_token": token, "token_type": "bearer"}


# -------- BOOTSTRAP ADMIN --------
@router.post(
    "/bootstrap-admin",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Crea el primer usuario administrador (solo si no existen usuarios)",
    responses={
        400: {"description": "Ya existen usuarios; operación no permitida"},
        409: {"description": "El email ya existe (en caso de carrera/race)"},
    },
)
def bootstrap_admin(
    payload: UserCreate,
    db: Annotated[Session, Depends(get_db)],
) -> UserOut:
    """
    Crea el primer **usuario admin** si la tabla está vacía.
    Útil para inicialización del sistema.
    """
    # Si ya hay usuarios, aborta
    if db.query(User).count() > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Users already exist")

    # (Opcional) valida que no exista ese email por carrera
    if db.query(User).filter(User.email == payload.email).first() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        role=UserRole.admin,
        hashed_password=get_password_hash(payload.password),
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        # Evita filtrar detalles del motor/driver
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create admin user")

    return user
