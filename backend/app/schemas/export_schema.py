# Pydantic schemas for export request/response
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExportCreateRequest(BaseModel):
    project_id: str
    engine_type: Optional[str] = None
    asset_ids: Optional[list[str]] = None


class ExportPackageResponse(BaseModel):
    id: str
    project_id: str
    status: str
    file_path: Optional[str] = None
    engine_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
