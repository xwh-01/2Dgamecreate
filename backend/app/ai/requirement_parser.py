# Natural language requirement parser using AI
from dataclasses import dataclass, field
from typing import Optional

from ..domain.enums.asset_type import AssetType


@dataclass
class ParseRequirementInput:
    user_input: str
    extra_params: dict = field(default_factory=dict)
    asset_type: Optional[AssetType] = None
    size: Optional[str] = None


@dataclass
class ParsedRequirement:
    asset_type: Optional[AssetType] = None
    subject: str = ""
    style_hint: str = ""
    size: Optional[str] = None
    direction: Optional[str] = None
    background: Optional[str] = None
    usage: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "asset_type": self.asset_type.value if self.asset_type else None,
            "subject": self.subject,
            "style_hint": self.style_hint,
            "size": self.size,
            "direction": self.direction,
            "background": self.background,
            "usage": self.usage,
        }


class RequirementParser:
    def parse(self, input_data: ParseRequirementInput) -> ParsedRequirement:
        raise NotImplementedError
