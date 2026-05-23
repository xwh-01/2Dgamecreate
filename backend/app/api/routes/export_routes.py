# Asset export and packaging API endpoints
from fastapi import APIRouter, Depends

from ...schemas.export_schema import ExportCreateRequest, ExportPackageResponse

router = APIRouter(tags=["exports"])


def get_export_service():
    raise NotImplementedError


@router.post("/api/projects/{project_id}/exports", response_model=ExportPackageResponse)
def create_export(project_id: str, body: ExportCreateRequest, service=Depends(get_export_service)):
    raise NotImplementedError


@router.get("/api/exports/{export_id}", response_model=ExportPackageResponse)
def get_export(export_id: str, service=Depends(get_export_service)):
    raise NotImplementedError
