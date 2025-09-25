from sqlalchemy import String, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.models.base import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    start_at: Mapped[datetime]
    end_at: Mapped[datetime]

    # scope: class-level event or child-specific
    class_group_id: Mapped[int | None] = mapped_column(ForeignKey("class_groups.id", ondelete="CASCADE"))
    child_id: Mapped[int | None] = mapped_column(ForeignKey("children.id", ondelete="CASCADE"))

    class_group = relationship("ClassGroup")
    child = relationship("Child")