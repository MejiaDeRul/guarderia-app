from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Child(Base):
    __tablename__ = "children"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120))
    last_name: Mapped[str] = mapped_column(String(120))
    parent_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    parent = relationship("User", back_populates="children")
    enrollments: Mapped[list["Enrollment"]] = relationship("Enrollment", back_populates="child", cascade="all, delete-orphan")