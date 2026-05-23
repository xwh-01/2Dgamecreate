# Prompt construction and optimization logic
from dataclasses import dataclass
from typing import Optional

from ..domain.enums.asset_type import AssetType
from ..domain.entities.style_profile import StyleProfile
from .requirement_parser import ParsedRequirement


@dataclass
class PromptPackage:
    base_prompt: str = ""
    asset_type_rules: str = ""
    style_profile_rules: str = ""
    technical_rules: str = ""
    engine_compatibility_rules: str = ""
    negative_prompt: str = ""

    def to_full_prompt(self) -> str:
        sections = [
            self.base_prompt,
            self.asset_type_rules,
            self.style_profile_rules,
            self.technical_rules,
            self.engine_compatibility_rules,
        ]
        return ", ".join(s for s in sections if s)

    def to_full_negative_prompt(self) -> str:
        return self.negative_prompt


class PromptBuilder:
    ASSET_TYPE_RULES: dict[AssetType, str] = {
        AssetType.CHARACTER: "",
        AssetType.PROP: "",
        AssetType.TILE: "",
        AssetType.UI_ICON: "",
        AssetType.EFFECT: "",
    }

    ENGINE_COMPATIBILITY_RULES = ""

    def build(
        self,
        parsed: ParsedRequirement,
        style_profile: Optional[StyleProfile] = None,
    ) -> PromptPackage:
        raise NotImplementedError

    def _build_base_prompt(self, parsed: ParsedRequirement) -> str:
        raise NotImplementedError

    def _get_asset_type_rules(self, asset_type: AssetType) -> str:
        raise NotImplementedError

    def _get_style_profile_rules(self, style_profile: Optional[StyleProfile]) -> str:
        raise NotImplementedError

    def _get_technical_rules(self, parsed: ParsedRequirement) -> str:
        raise NotImplementedError

    def _get_negative_prompt(self, style_profile: Optional[StyleProfile]) -> str:
        raise NotImplementedError
