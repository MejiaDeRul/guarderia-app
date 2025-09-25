from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    teacher = "teacher"
    parent = "parent"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), index=True)

    # relations
    children: Mapped[list["Child"]] = relationship("Child", back_populates="parent")