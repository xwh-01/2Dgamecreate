# Style profile management API endpoints
from fastapi import APIRouter, Depends

from ...schemas.style_schema import StyleProfileCreate, StyleProfileResponse, StyleProfileUpdate

router = APIRouter(prefix="/api/projects/{project_id}/style", tags=["styles"])


def get_style_service():
    raise NotImplementedError


@router.post("", response_model=StyleProfileResponse)
def create_style(project_id: str, body: StyleProfileCreate, service=Depends(get_style_service)):
    raise NotImplementedError


@router.get("", response_model=StyleProfileResponse)
def get_style(project_id: str, service=Depends(get_style_service)):
    raise NotImplementedError


@router.put("", response_model=StyleProfileResponse)
def update_style(project_id: str, body: StyleProfileUpdate, service=Depends(get_style_service)):
    raise NotImplementedError
