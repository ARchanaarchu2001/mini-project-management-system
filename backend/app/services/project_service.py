from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.project import Project
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.project_repository = ProjectRepository(db)

    def create_project(self, payload: ProjectCreate, current_user: User) -> Project:
        project = Project(
            name=payload.name,
            description=payload.description,
            created_by=current_user.id,
        )
        self.project_repository.create(project)
        self.db.commit()
        return project

    def list_projects(self) -> list[Project]:
        return self.project_repository.get_all()

    def update_project(self, project_id: int, payload: ProjectUpdate) -> Project:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundException("Project not found")

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(project, field, value)

        self.db.commit()
        self.db.refresh(project)
        return project

    def delete_project(self, project_id: int) -> None:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundException("Project not found")

        self.project_repository.delete(project)
        self.db.commit()
