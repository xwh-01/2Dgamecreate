# Asset domain entity
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from ..enums.asset_type import AssetType


@dataclass
class Asset:
    id: str
    project_id: str
    task_id: str
    name: str
    asset_type: AssetType
    file_path: str
    preview_url: Optional[str] = None
    width: int = 0
    height: int = 0
    format: str = "png"
    transparent: bool = False
    metadata: Optional[Any] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
