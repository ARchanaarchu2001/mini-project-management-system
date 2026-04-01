from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.models.task import TaskStatus


class TaskBase(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    project_id: int
    assigned_to: int | None = None
    due_date: date | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = None
    status: TaskStatus | None = None
    project_id: int | None = None
    assigned_to: int | None = None
    due_date: date | None = None


class TaskResponse(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TaskFilterParams(BaseModel):
    status: TaskStatus | None = None
    project_id: int | None = None
    assigned_to: int | None = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)


class TaskListResponse(BaseModel):
    items: list[TaskResponse]
    page: int
    limit: int
    total: int
