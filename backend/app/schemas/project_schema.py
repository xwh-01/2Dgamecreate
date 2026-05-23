# Pydantic schemas for project request/response
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    style_profile_id: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    style_profile_id: Optional[str] = None


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    style_profile_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    items: list[ProjectResponse]
    total: int
