# Project CRUD API endpoints
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...dependencies import get_project_service
from ...services.project_service import ProjectService

router = APIRouter(prefix="/api/projects", tags=["projects"])


class ProjectCreateBody(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectUpdateBody(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


@router.post("")
def create_project(body: ProjectCreateBody, service: ProjectService = Depends(get_project_service)):
    project = service.create_project(body.name, body.description)
    return {
        "success": True,
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
        },
    }


@router.get("")
def list_projects(service: ProjectService = Depends(get_project_service)):
    projects = service.list_projects()
    return {
        "success": True,
        "projects": [
            {"id": p.id, "name": p.name, "description": p.description}
            for p in projects
        ],
    }


@router.get("/{project_id}")
def get_project(project_id: str, service: ProjectService = Depends(get_project_service)):
    project = service.get_project(project_id)
    if project is None:
        return {"success": False, "error": "Project not found"}
    return {
        "success": True,
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "style_profile_id": project.style_profile_id,
        },
    }


@router.put("/{project_id}")
def update_project(project_id: str, body: ProjectUpdateBody, service: ProjectService = Depends(get_project_service)):
    data = {}
    if body.name is not None:
        data["name"] = body.name
    if body.description is not None:
        data["description"] = body.description
    project = service.update_project(project_id, data)
    if project is None:
        return {"success": False, "error": "Project not found"}
    return {"success": True, "project": {"id": project.id, "name": project.name, "description": project.description}}
