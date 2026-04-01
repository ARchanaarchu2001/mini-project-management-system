import enum
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(
            TaskStatus,
            name="task_status",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
        default=TaskStatus.TODO,
        nullable=False,
    )
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    assigned_to: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")
