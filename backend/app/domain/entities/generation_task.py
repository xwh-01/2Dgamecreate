# Generation task domain entity
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Union

from ..enums.asset_type import AssetType
from ..enums.task_status import TaskStatus


@dataclass
class GenerationTask:
    id: str
    project_id: str
    asset_type: Union[AssetType, str]
    status: Union[TaskStatus, str] = TaskStatus.PENDING
    user_input: str = ""
    parsed_requirement: Optional[Any] = None
    final_prompt: Optional[str] = None
    model_name: Optional[str] = None
    size: Optional[str] = None
    error_message: Optional[str] = None
    result_asset_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if isinstance(self.asset_type, str):
            self.asset_type = AssetType(self.asset_type)
        if isinstance(self.status, str):
            self.status = TaskStatus(self.status)
