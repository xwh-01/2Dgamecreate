# Project data access layer
from typing import Optional

from ..db.session import get_session
from ..domain.entities.project import Project
from ..utils.time import utcnow


class ProjectRepository:
    def get_by_id(self, project_id: str) -> Optional[Project]:
        data = get_session().projects.get(project_id)
        if data is None:
            return None
        return Project(**data)

    def list_all(self) -> list[Project]:
        return [Project(**v) for v in get_session().projects.get_all().values()]

    def create(self, project: Project) -> Project:
        project.created_at = utcnow()
        project.updated_at = utcnow()
        get_session().projects.set(project.id, {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "style_profile_id": project.style_profile_id,
            "created_at": project.created_at.isoformat(),
            "updated_at": project.updated_at.isoformat(),
        })
        return project

    def update(self, project_id: str, data_dict: dict) -> Optional[Project]:
        existing = get_session().projects.get(project_id)
        if existing is None:
            return None
        existing.update(data_dict)
        existing["updated_at"] = utcnow().isoformat()
        get_session().projects.set(project_id, existing)
        return Project(**existing)

    def delete(self, project_id: str) -> bool:
        return get_session().projects.delete(project_id)
