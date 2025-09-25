from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Enrollment(Base):
    __tablename__ = "enrollments"
    __table_args__ = (UniqueConstraint("child_id", "class_group_id", name="uq_child_class"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    child_id: Mapped[int] = mapped_column(ForeignKey("children.id", ondelete="CASCADE"))
    class_group_id: Mapped[int] = mapped_column(ForeignKey("class_groups.id", ondelete="CASCADE"))

    child = relationship("Child", back_populates="enrollments")
    class_group = relationship("ClassGroup", back_populates="enrollments")