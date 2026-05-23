# Project business logic service
from typing import Optional

from ..domain.entities.project import Project
from ..repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, project_repo: ProjectRepository):
        self.repo = project_repo

    def create_project(self, name: str, description: Optional[str] = None) -> Project:
        raise NotImplementedError

    def get_project(self, project_id: str) -> Optional[Project]:
        raise NotImplementedError

    def list_projects(self) -> list[Project]:
        raise NotImplementedError

    def update_project(self, project_id: str, data: dict) -> Optional[Project]:
        raise NotImplementedError

    def delete_project(self, project_id: str) -> bool:
        raise NotImplementedError
