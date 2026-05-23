# Project CRUD API endpoints
from typing import Optional

from fastapi import APIRouter, Depends

from ...schemas.project_schema import ProjectCreate, ProjectListResponse, ProjectResponse, ProjectUpdate

router = APIRouter(prefix="/api/projects", tags=["projects"])


def get_project_service():
    raise NotImplementedError


@router.post("", response_model=ProjectResponse)
def create_project(body: ProjectCreate, service=Depends(get_project_service)):
    raise NotImplementedError


@router.get("", response_model=ProjectListResponse)
def list_projects(service=Depends(get_project_service)):
    raise NotImplementedError


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, service=Depends(get_project_service)):
    raise NotImplementedError


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: str, body: ProjectUpdate, service=Depends(get_project_service)):
    raise NotImplementedError
