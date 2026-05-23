# Export package domain entity
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class ExportStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass
class ExportPackage:
    id: str
    project_id: str
    status: ExportStatus = ExportStatus.PENDING
    file_path: Optional[str] = None
    engine_type: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
