# Asset export and packaging API endpoints
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...dependencies import get_export_service
from ...services.export_service import ExportService

router = APIRouter(tags=["exports"])


class ExportCreateBody(BaseModel):
    project_id: str
    engine_type: Optional[str] = None
    asset_ids: Optional[list[str]] = None


@router.post("/api/projects/{project_id}/exports")
def create_export(project_id: str, body: ExportCreateBody, service: ExportService = Depends(get_export_service)):
    pkg = service.create_export(project_id, body.engine_type)
    return {
        "success": True,
        "export": {
            "id": pkg.id,
            "project_id": pkg.project_id,
            "status": pkg.status.value,
            "engine_type": pkg.engine_type,
        },
    }


@router.get("/api/exports/{export_id}")
def get_export(export_id: str, service: ExportService = Depends(get_export_service)):
    pkg = service.get_export(export_id)
    if pkg is None:
        return {"success": False, "error": "Export not found"}
    return {
        "success": True,
        "export": {
            "id": pkg.id,
            "project_id": pkg.project_id,
            "status": pkg.status.value,
            "file_path": pkg.file_path,
            "engine_type": pkg.engine_type,
        },
    }
