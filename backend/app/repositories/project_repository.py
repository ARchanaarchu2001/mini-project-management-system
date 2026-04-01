from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, project: Project) -> Project:
        self.db.add(project)
        self.db.flush()
        self.db.refresh(project)
        return project

    def get_by_id(self, project_id: int) -> Project | None:
        return self.db.get(Project, project_id)

    def get_all(self) -> list[Project]:
        return list(self.db.scalars(select(Project).order_by(Project.id.desc())).all())

    def delete(self, project: Project) -> None:
        self.db.delete(project)
