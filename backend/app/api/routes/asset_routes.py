# Asset retrieval and metadata API endpoints
import os

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, Response

from ...dependencies import get_asset_service, get_file_storage, get_path_builder
from ...services.asset_service import AssetService
from ...storage.file_storage import FileStorage

router = APIRouter(tags=["assets"])


@router.get("/api/projects/{project_id}/assets")
def list_project_assets(project_id: str, service: AssetService = Depends(get_asset_service)):
    assets = service.list_by_project(project_id)
    assets = sorted(assets, key=lambda a: a.created_at or "", reverse=True)
    return {
        "success": True,
        "assets": [
            {
                "id": a.id,
                "project_id": a.project_id,
                "task_id": a.task_id,
                "name": a.name,
                "asset_type": a.asset_type.value,
                "file_path": a.file_path,
                "preview_url": a.preview_url,
                "download_url": f"/api/download/{a.id}",
                "width": a.width,
                "height": a.height,
                "created_at": a.created_at if isinstance(a.created_at, str) else (a.created_at.isoformat() if a.created_at else ""),
                "metadata": a.metadata or {},
            }
            for a in assets
        ],
    }


@router.get("/api/assets/{asset_id}")
def get_asset(asset_id: str, service: AssetService = Depends(get_asset_service)):
    asset = service.get_asset(asset_id)
    if asset is None:
        return {"success": False, "error": "Asset not found"}
    return {
        "success": True,
        "asset": {
            "id": asset.id,
            "project_id": asset.project_id,
            "task_id": asset.task_id,
            "name": asset.name,
            "asset_type": asset.asset_type.value,
            "file_path": asset.file_path,
            "preview_url": asset.preview_url,
            "download_url": f"/api/download/{asset.id}",
            "width": asset.width,
            "height": asset.height,
            "created_at": asset.created_at if isinstance(asset.created_at, str) else (asset.created_at.isoformat() if asset.created_at else ""),
            "metadata": asset.metadata or {},
        },
    }


@router.get("/api/download/{asset_id}")
def download_asset(asset_id: str, service: AssetService = Depends(get_asset_service)):
    asset = service.get_asset(asset_id)
    if asset is None:
        return {"success": False, "error": "Asset not found"}

    builder = get_path_builder()
    storage = get_file_storage()
    full_path = storage._full_path(asset.file_path)

    if not os.path.exists(full_path):
        return Response(content=b"File not found", status_code=404)

    return FileResponse(
        path=full_path,
        media_type="image/png",
        filename=f"{asset.name}.png",
    )


@router.delete("/api/assets/{asset_id}")
def delete_asset(asset_id: str, service: AssetService = Depends(get_asset_service)):
    success = service.delete_asset(asset_id)
    if not success:
        return {"success": False, "error": "Asset not found or delete failed"}
    return {"success": True}


@router.get("/assets/{file_path:path}")
def serve_asset(file_path: str, storage: FileStorage = Depends(get_file_storage)):
    full_path = storage._full_path(file_path)
    if not os.path.exists(full_path):
        return Response(content=b"File not found", status_code=404)
    return FileResponse(path=full_path, media_type="image/png")
