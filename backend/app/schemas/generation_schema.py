# Pydantic schemas for generation task request/response
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel

from ..domain.enums.asset_type import AssetType
from ..domain.enums.task_status import TaskStatus


class ExtraParams(BaseModel):
    direction: Optional[str] = None
    background: Optional[str] = None
    usage: Optional[str] = None
    name: Optional[str] = None
    view: Optional[str] = None
    action: Optional[str] = None
    appearance: Optional[str] = None
    weapon: Optional[str] = None
    item_category: Optional[str] = None
    tile_type: Optional[str] = None
    material: Optional[str] = None
    seamless: Optional[str] = None
    icon_purpose: Optional[str] = None
    shape: Optional[str] = None
    effect_type: Optional[str] = None
    motion_feeling: Optional[str] = None


class GenerationCreateRequest(BaseModel):
    project_id: str
    asset_type: AssetType
    description: str
    size: Optional[str] = None
    quantity: int = 1
    extra_params: Optional[ExtraParams] = None


class GenerationTaskResponse(BaseModel):
    id: str
    project_id: str
    asset_type: AssetType
    status: TaskStatus
    user_input: str
    parsed_requirement: Optional[Any] = None
    final_prompt: Optional[str] = None
    model_name: Optional[str] = None
    size: Optional[str] = None
    error_message: Optional[str] = None
    result_asset_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True, "protected_namespaces": ()}


class GenerationTaskListResponse(BaseModel):
    items: list[GenerationTaskResponse]
    total: int
