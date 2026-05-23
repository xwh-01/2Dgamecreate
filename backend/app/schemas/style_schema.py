# Pydantic schemas for style profile request/response
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..domain.enums.art_style import ArtStyle
from ..domain.enums.view_type import ViewType


class StyleProfileCreate(BaseModel):
    project_id: str
    art_style: ArtStyle
    view_type: ViewType
    color_palette: Optional[str] = None
    outline_style: Optional[str] = None
    default_size: Optional[str] = None
    prompt_rules: Optional[str] = None
    negative_prompt_rules: Optional[str] = None


class StyleProfileUpdate(BaseModel):
    art_style: Optional[ArtStyle] = None
    view_type: Optional[ViewType] = None
    color_palette: Optional[str] = None
    outline_style: Optional[str] = None
    default_size: Optional[str] = None
    prompt_rules: Optional[str] = None
    negative_prompt_rules: Optional[str] = None


class StyleProfileResponse(BaseModel):
    id: str
    project_id: str
    art_style: ArtStyle
    view_type: ViewType
    color_palette: Optional[str] = None
    outline_style: Optional[str] = None
    default_size: Optional[str] = None
    prompt_rules: Optional[str] = None
    negative_prompt_rules: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
