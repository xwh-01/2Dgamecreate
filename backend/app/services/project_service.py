# Project business logic service
import uuid
from typing import Optional

from ..domain.entities.project import Project
from ..repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, project_repo: ProjectRepository):
        self.repo = project_repo

    def create_project(self, name: str, description: Optional[str] = None) -> Project:
        project = Project(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
        )
        return self.repo.create(project)

    def get_project(self, project_id: str) -> Optional[Project]:
        return self.repo.get_by_id(project_id)

    def list_projects(self) -> list[Project]:
        return self.repo.list_all()

    def update_project(self, project_id: str, data: dict) -> Optional[Project]:
        return self.repo.update(project_id, data)

    def delete_project(self, project_id: str) -> bool:
        return self.repo.delete(project_id)
