# Pydantic schemas for asset request/response
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel

from ..domain.enums.asset_type import AssetType


class AssetUpdate(BaseModel):
    name: Optional[str] = None


class AssetResponse(BaseModel):
    id: str
    project_id: str
    task_id: str
    name: str
    asset_type: AssetType
    file_path: str
    preview_url: Optional[str] = None
    width: int
    height: int
    format: str
    transparent: bool
    metadata: Optional[Any] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AssetListResponse(BaseModel):
    items: list[AssetResponse]
    total: int
