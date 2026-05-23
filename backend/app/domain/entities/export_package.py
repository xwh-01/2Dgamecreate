# Export package domain entity
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Union


class ExportStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass
class ExportPackage:
    id: str
    project_id: str
    status: Union[ExportStatus, str] = ExportStatus.PENDING
    file_path: Optional[str] = None
    engine_type: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if isinstance(self.status, str):
            self.status = ExportStatus(self.status)
