from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services.project_service import ProjectService
from app.utils.dependencies import get_admin_user, get_current_user

router = APIRouter()


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_admin_user),
) -> ProjectResponse:
    return ProjectService(db).create_project(payload, current_user)


@router.get("", response_model=list[ProjectResponse])
def list_projects(
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
) -> list[ProjectResponse]:
    return ProjectService(db).list_projects()


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(get_admin_user),
) -> ProjectResponse:
    return ProjectService(db).update_project(project_id, payload)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(get_admin_user),
) -> Response:
    ProjectService(db).delete_project(project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
