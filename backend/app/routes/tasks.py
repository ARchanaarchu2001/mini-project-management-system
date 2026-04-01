from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.task import TaskStatus
from app.schemas.task import TaskCreate, TaskFilterParams, TaskListResponse, TaskResponse, TaskUpdate
from app.services.task_service import TaskService
from app.utils.dependencies import get_current_user

router = APIRouter()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
) -> TaskResponse:
    return TaskService(db).create_task(payload)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
) -> TaskResponse:
    return TaskService(db).update_task(task_id, payload)


@router.get("", response_model=TaskListResponse)
def list_tasks(
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    project_id: int | None = Query(default=None),
    assigned_to: int | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
) -> TaskListResponse:
    filters = TaskFilterParams(
        status=status_filter,
        project_id=project_id,
        assigned_to=assigned_to,
        page=page,
        limit=limit,
    )
    return TaskService(db).list_tasks(filters)
