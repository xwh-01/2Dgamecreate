# Style profile domain entity
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union

from ..enums.art_style import ArtStyle
from ..enums.view_type import ViewType


@dataclass
class StyleProfile:
    id: str
    project_id: str
    art_style: Union[ArtStyle, str]
    view_type: Union[ViewType, str]
    color_palette: Optional[str] = None
    outline_style: Optional[str] = None
    default_size: Optional[str] = None
    prompt_rules: Optional[str] = None
    negative_prompt_rules: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if isinstance(self.art_style, str):
            self.art_style = ArtStyle(self.art_style)
        if isinstance(self.view_type, str):
            self.view_type = ViewType(self.view_type)
