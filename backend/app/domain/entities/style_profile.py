# Style profile domain entity
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ..enums.art_style import ArtStyle
from ..enums.view_type import ViewType


@dataclass
class StyleProfile:
    id: str
    project_id: str
    art_style: ArtStyle
    view_type: ViewType
    color_palette: Optional[str] = None
    outline_style: Optional[str] = None
    default_size: Optional[str] = None
    prompt_rules: Optional[str] = None
    negative_prompt_rules: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
