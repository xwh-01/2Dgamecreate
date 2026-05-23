# Asset generation trigger and management API endpoints
from fastapi import APIRouter, Depends

from ...schemas.generation_schema import (
    GenerationCreateRequest,
    GenerationTaskListResponse,
    GenerationTaskResponse,
)

router = APIRouter(tags=["generations"])


def get_generation_service():
    raise NotImplementedError


@router.post("/api/generations", response_model=GenerationTaskResponse)
def create_generation(body: GenerationCreateRequest, service=Depends(get_generation_service)):
    raise NotImplementedError


@router.get("/api/generations/{task_id}", response_model=GenerationTaskResponse)
def get_generation(task_id: str, service=Depends(get_generation_service)):
    raise NotImplementedError


@router.get("/api/projects/{project_id}/generations", response_model=GenerationTaskListResponse)
def list_project_generations(project_id: str, service=Depends(get_generation_service)):
    raise NotImplementedError
