# Project domain entity
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Project:
    id: str
    name: str
    description: Optional[str] = None
    style_profile_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
