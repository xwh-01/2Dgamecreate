# Asset domain entity
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Union

from ..enums.asset_type import AssetType


@dataclass
class Asset:
    id: str
    project_id: str
    task_id: str
    name: str
    asset_type: Union[AssetType, str]
    file_path: str
    preview_url: Optional[str] = None
    width: int = 0
    height: int = 0
    format: str = "png"
    transparent: bool = False
    metadata: Optional[Any] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if isinstance(self.asset_type, str):
            self.asset_type = AssetType(self.asset_type)
