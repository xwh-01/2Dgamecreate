# Project data access layer
from typing import Optional

from ..domain.entities.project import Project


class ProjectRepository:
    def get_by_id(self, project_id: str) -> Optional[Project]:
        raise NotImplementedError

    def list_all(self) -> list[Project]:
        raise NotImplementedError

    def create(self, project: Project) -> Project:
        raise NotImplementedError

    def update(self, project_id: str, data: dict) -> Optional[Project]:
        raise NotImplementedError

    def delete(self, project_id: str) -> bool:
        raise NotImplementedError
