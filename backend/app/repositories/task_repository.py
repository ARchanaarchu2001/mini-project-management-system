from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.task import Task, TaskStatus


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task) -> Task:
        self.db.add(task)
        self.db.flush()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Task | None:
        return self.db.get(Task, task_id)

    def get_filtered(
        self,
        *,
        status: TaskStatus | None = None,
        project_id: int | None = None,
        assigned_to: int | None = None,
        offset: int = 0,
        limit: int = 10,
    ) -> tuple[list[Task], int]:
        filters = []
        if status is not None:
            filters.append(Task.status == status)
        if project_id is not None:
            filters.append(Task.project_id == project_id)
        if assigned_to is not None:
            filters.append(Task.assigned_to == assigned_to)

        items = list(
            self.db.scalars(
                select(Task)
                .where(*filters)
                .order_by(Task.id.desc())
                .offset(offset)
                .limit(limit)
            ).all()
        )
        total = self.db.scalar(select(func.count()).select_from(Task).where(*filters)) or 0
        return items, total
