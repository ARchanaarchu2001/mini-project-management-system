from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestException, NotFoundException
from app.models.task import Task
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.schemas.task import TaskCreate, TaskFilterParams, TaskListResponse, TaskUpdate


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repository = TaskRepository(db)
        self.project_repository = ProjectRepository(db)
        self.user_repository = UserRepository(db)

    def create_task(self, payload: TaskCreate) -> Task:
        self._validate_relations(payload.project_id, payload.assigned_to)
        task = Task(**payload.model_dump())
        self.task_repository.create(task)
        self.db.commit()
        return task

    def update_task(self, task_id: int, payload: TaskUpdate) -> Task:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundException("Task not found")

        updates = payload.model_dump(exclude_unset=True)
        self._validate_relations(
            updates.get("project_id", task.project_id),
            updates.get("assigned_to", task.assigned_to),
        )
        for field, value in updates.items():
            setattr(task, field, value)

        self.db.commit()
        self.db.refresh(task)
        return task

    def list_tasks(self, filters: TaskFilterParams) -> TaskListResponse:
        offset = (filters.page - 1) * filters.limit
        items, total = self.task_repository.get_filtered(
            status=filters.status,
            project_id=filters.project_id,
            assigned_to=filters.assigned_to,
            offset=offset,
            limit=filters.limit,
        )
        return TaskListResponse(
            items=items,
            page=filters.page,
            limit=filters.limit,
            total=total,
        )

    def _validate_relations(self, project_id: int, assigned_to: int | None) -> None:
        if self.project_repository.get_by_id(project_id) is None:
            raise BadRequestException("Project does not exist")
        if assigned_to is not None and self.user_repository.get_by_id(assigned_to) is None:
            raise BadRequestException("Assigned user does not exist")
