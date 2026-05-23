# Prompt construction and optimization logic
from dataclasses import dataclass
from typing import Optional

from ..domain.enums.asset_type import AssetType
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


STYLE_RULES = {
    "pixel_art": "pixel art, crisp edges, limited color palette, no realistic painting, no anti-aliasing",
    "cartoon": "cartoon style, clean outlines, flat shading, cel shading, animated style",
    "hand_drawn": "hand drawn style, sketchy lines, artistic, illustration, traditional media",
}

ASSET_TYPE_RULES = {
    AssetType.CHARACTER: "single 2D game character sprite, full body, centered, transparent background, clean readable silhouette, suitable for Unity Godot 2D game",
    AssetType.PROP: "single 2D game item icon, centered, transparent background, no text, clean readable silhouette, game prop",
    AssetType.TILE: "seamless 2D tile texture, repeatable, top-down view, suitable for tile map, no seams at edges",
    AssetType.UI_ICON: "2D game UI icon, centered, transparent background, high contrast, no text, clean design",
    AssetType.EFFECT: "2D game visual effect sprite, transparent background, centered, particle or energy effect style",
}

DEFAULT_NEGATIVE = "text, watermark, logo, blurry, noisy background, realistic photo, 3D render, signature, artist name, complex background"


class PromptBuilder:
    def build(
        self,
        parsed: ParsedRequirement,
        style_profile: Optional[dict] = None,
    ) -> PromptPackage:
        pkg = PromptPackage()
        pkg.base_prompt = self._build_base_prompt(parsed)
        pkg.asset_type_rules = self._get_asset_type_rules(
            parsed.asset_type or AssetType.CHARACTER
        )
        pkg.style_profile_rules = self._get_style_profile_rules(style_profile)
        pkg.technical_rules = self._get_technical_rules(parsed)
        pkg.engine_compatibility_rules = self._get_engine_rules()
        pkg.negative_prompt = self._get_negative_prompt(style_profile)
        return pkg

    def _build_base_prompt(self, parsed: ParsedRequirement) -> str:
        parts = [parsed.subject]
        if parsed.style_hint:
            parts.append(parsed.style_hint)
        if parsed.direction:
            parts.append(f"facing {parsed.direction}")
        if parsed.usage:
            usage_map = {
                "player_sprite": "player character",
                "enemy_sprite": "enemy character",
                "npc_sprite": "NPC character",
                "ui_element": "UI element",
                "environment": "environment asset",
                "prop": "game prop",
            }
            parts.append(usage_map.get(parsed.usage, parsed.usage))
        return " ".join(parts)

    def _get_asset_type_rules(self, asset_type: AssetType) -> str:
        return ASSET_TYPE_RULES.get(asset_type, ASSET_TYPE_RULES[AssetType.PROP])

    def _get_style_profile_rules(self, style_profile: Optional[dict]) -> str:
        if style_profile is None:
            return ""
        art_style = style_profile.get("art_style", "")
        rules = STYLE_RULES.get(art_style, "")
        custom = style_profile.get("prompt_rules", "")
        if custom:
            rules = f"{rules}, {custom}"
        size = style_profile.get("default_size", "")
        if size:
            rules = f"{rules}, {size}"
        return rules

    def _get_technical_rules(self, parsed: ParsedRequirement) -> str:
        parts = []
        if parsed.size:
            parts.append(parsed.size)
        if parsed.background:
            if parsed.background == "transparent":
                parts.append("transparent background, alpha channel")
            else:
                parts.append(f"{parsed.background} background")
        else:
            parts.append("transparent background")
        parts.append("game-ready sprite sheet compatible")
        return ", ".join(parts)

    def _get_engine_rules(self) -> str:
        return "pixel perfect, centered pivot, no shadow, isolated on transparent, ready for Unity Godot sprite import"

    def _get_negative_prompt(self, style_profile: Optional[dict]) -> str:
        neg = DEFAULT_NEGATIVE
        if style_profile and style_profile.get("negative_prompt_rules"):
            neg = f"{neg}, {style_profile['negative_prompt_rules']}"
        return neg
