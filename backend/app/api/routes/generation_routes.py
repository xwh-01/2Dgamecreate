# Asset generation trigger and management API endpoints
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...dependencies import get_generation_service
from ...domain.enums.asset_type import AssetType
from ...schemas.generation_schema import GenerationCreateRequest
from ...services.generation_service import GenerationService

router = APIRouter(tags=["generations"])


class ExtraParamsModel(BaseModel):
    direction: Optional[str] = None
    background: Optional[str] = None
    usage: Optional[str] = None


class GenerationCreateBody(BaseModel):
    project_id: str
    asset_type: str
    description: str
    size: Optional[str] = None
    quantity: int = 1
    extra_params: Optional[ExtraParamsModel] = None


ASSET_TYPE_MAP = {
    "character": AssetType.CHARACTER,
    "item": AssetType.PROP,
    "tile": AssetType.TILE,
    "ui_icon": AssetType.UI_ICON,
}


@router.post("/api/generations")
def create_generation(body: GenerationCreateBody, service: GenerationService = Depends(get_generation_service)):
    asset_type = ASSET_TYPE_MAP.get(body.asset_type, AssetType.CHARACTER)
    from ...schemas.generation_schema import ExtraParams

    extra = None
    if body.extra_params:
        extra = ExtraParams(
            direction=body.extra_params.direction,
            background=body.extra_params.background,
            usage=body.extra_params.usage,
        )

    request = GenerationCreateRequest(
        project_id=body.project_id,
        asset_type=asset_type,
        description=body.description,
        size=body.size,
        quantity=body.quantity,
        extra_params=extra,
    )

    task = service.create_task(request)

    try:
        ctx = service.run_task(task.id)
    except Exception as e:
        return {
            "success": False,
            "task": {
                "id": task.id,
                "status": "failed",
                "asset_id": None,
                "preview_url": None,
                "download_url": None,
                "error_message": str(e),
            },
        }

    if ctx.asset_record and ctx.asset_record.preview_url:
        preview_url = ctx.asset_record.preview_url
        download_url = f"/api/download/{ctx.asset_record.id}"
        return {
            "success": True,
            "task": {
                "id": task.id,
                "status": "succeeded",
                "asset_id": ctx.asset_record.id,
                "preview_url": preview_url,
                "download_url": download_url,
                "error_message": None,
            },
        }
    else:
        return {
            "success": False,
            "task": {
                "id": task.id,
                "status": "failed",
                "asset_id": None,
                "preview_url": None,
                "download_url": None,
                "error_message": ctx.error_message or "Unknown error",
            },
        }


@router.get("/api/generations/{task_id}")
def get_generation(task_id: str, service: GenerationService = Depends(get_generation_service)):
    task = service.get_task(task_id)
    if task is None:
        return {"success": False, "error": "Task not found"}

    preview_url = None
    download_url = None
    if task.result_asset_id:
        from ...dependencies import get_asset_service
        asset = get_asset_service().get_asset(task.result_asset_id)
        if asset:
            preview_url = asset.preview_url
            download_url = f"/api/download/{asset.id}"

    return {
        "success": True,
        "task": {
            "id": task.id,
            "status": task.status.value,
            "asset_id": task.result_asset_id,
            "preview_url": preview_url,
            "download_url": download_url,
            "error_message": task.error_message,
        },
    }


@router.get("/api/projects/{project_id}/generations")
def list_project_generations(project_id: str, service: GenerationService = Depends(get_generation_service)):
    tasks = service.list_by_project(project_id)
    return {
        "success": True,
        "generations": [
            {
                "id": t.id,
                "status": t.status.value,
                "asset_type": t.asset_type.value,
                "user_input": t.user_input,
                "result_asset_id": t.result_asset_id,
                "error_message": t.error_message,
                "created_at": t.created_at.isoformat() if t.created_at else "",
            }
            for t in sorted(tasks, key=lambda x: x.created_at or "", reverse=True)
        ],
    }
