from app.models.task import TaskStatus
from app.schemas.task import TaskFilterParams


def test_task_filter_defaults() -> None:
    filters = TaskFilterParams()

    assert filters.page == 1
    assert filters.limit == 10
    assert filters.status is None


def test_task_filter_accepts_status_enum() -> None:
    filters = TaskFilterParams(status=TaskStatus.IN_PROGRESS, project_id=3, assigned_to=7)

    assert filters.status == TaskStatus.IN_PROGRESS
    assert filters.project_id == 3
    assert filters.assigned_to == 7
