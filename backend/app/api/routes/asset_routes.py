# Asset retrieval and metadata API endpoints
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from ...schemas.asset_schema import AssetListResponse, AssetResponse

router = APIRouter(tags=["assets"])


def get_asset_service():
    raise NotImplementedError


@router.get("/api/projects/{project_id}/assets", response_model=AssetListResponse)
def list_project_assets(project_id: str, service=Depends(get_asset_service)):
    raise NotImplementedError


@router.get("/api/assets/{asset_id}", response_model=AssetResponse)
def get_asset(asset_id: str, service=Depends(get_asset_service)):
    raise NotImplementedError


@router.get("/api/assets/{asset_id}/download")
def download_asset(asset_id: str, service=Depends(get_asset_service)):
    raise NotImplementedError


@router.delete("/api/assets/{asset_id}")
def delete_asset(asset_id: str, service=Depends(get_asset_service)):
    raise NotImplementedError
