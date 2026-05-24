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
    "pixel_art": (
        "pixel art sprite, hard pixel edges, low-resolution game asset, limited color palette, "
        "clean dark outline, simple readable silhouette, readable at 64x64 or 128x128, "
        "no smooth gradients, no soft 3D lighting, no anti-aliasing, crisp pixel edges, "
        "suitable for Unity 2D sprite, pixelated shading only, flat 2D game art"
    ),
    "cartoon": (
        "cute stylized 2D game sprite, simple rounded shapes, clean outline, readable silhouette, "
        "flat shading, cel shading, animated style, no 3D toy-like rendering, no plastic look, "
        "no soft realistic lighting, 2D flat cartoon style"
    ),
    "hand_drawn": (
        "hand drawn style, sketchy lines, artistic, illustration, traditional media, "
        "2D game art, no 3D rendering, no smooth gradients"
    ),
}

ASSET_TYPE_RULES = {
    AssetType.CHARACTER: "single 2D game character sprite, full body, centered, transparent background, clean readable silhouette, suitable for Unity Godot 2D game, game-ready character, no background clutter, isolated on transparent",
    AssetType.ENEMY: "single 2D game enemy sprite, full body, centered, transparent background, clean readable silhouette, suitable for Unity Godot 2D game, game-ready enemy character, no background clutter, isolated on transparent",
    AssetType.PROP: "single 2D game item icon, centered, transparent background, no text, clean readable silhouette, game prop, inventory item, isolated on transparent",
    AssetType.TILE: "2D game tile texture, top-down view, edge-matchable, no perspective distortion, suitable for tile map, game-ready tile",
    AssetType.UI_ICON: "clean 2D game UI icon, centered, transparent background, high contrast, simple readable shape, clean design, game interface element",
    AssetType.EFFECT: "2D game VFX sprite, transparent background, centered, high contrast, readable in game, particle or energy effect style, game visual effect frame, isolated on transparent",
}

DEFAULT_NEGATIVE = (
    "text, watermark, logo, blurry, noisy background, realistic photo, 3D render, "
    "3d render, plastic toy, toy-like rendering, smooth gradient, soft realistic lighting, "
    "realistic texture, complex scene, ground shadow, floating gray background, blurry edges, "
    "signature, artist name, complex background, no cropped body, no multiple subjects, "
    "no extra limbs, no messy details"
)


class PromptBuilder:
    def build(
        self,
        parsed: ParsedRequirement,
        style_profile: Optional[dict] = None,
    ) -> PromptPackage:
        pkg = PromptPackage()
        pkg.base_prompt = self._build_base_prompt(parsed, style_profile)
        pkg.asset_type_rules = self._get_asset_type_rules(parsed)
        pkg.style_profile_rules = self._get_style_profile_rules(style_profile)
        pkg.technical_rules = self._get_technical_rules(parsed)
        pkg.engine_compatibility_rules = self._get_engine_rules()
        pkg.negative_prompt = self._get_negative_prompt(style_profile)
        return pkg

    def _is_slime(self, parsed: ParsedRequirement) -> bool:
        if parsed.asset_type != AssetType.ENEMY:
            return False
        text = (parsed.subject + " " + (parsed.name or "") + " " + (parsed.appearance or "")).lower()
        return any(kw in text for kw in ("slime", "slime", "圆滚滚", "slime enemy", "blob"))

    def _build_base_prompt(self, parsed: ParsedRequirement, style_profile: Optional[dict] = None) -> str:
        asset_type = parsed.asset_type

        if asset_type in (AssetType.CHARACTER, AssetType.ENEMY):
            return self._build_character_prompt(parsed, style_profile)
        if asset_type == AssetType.PROP:
            return self._build_item_prompt(parsed)
        if asset_type == AssetType.TILE:
            return self._build_tile_prompt(parsed)
        if asset_type == AssetType.UI_ICON:
            return self._build_ui_icon_prompt(parsed)
        if asset_type == AssetType.EFFECT:
            return self._build_effect_prompt(parsed)

        parts = [parsed.subject]
        if parsed.direction:
            parts.append(f"facing {parsed.direction}")
        return " ".join(parts)

    def _build_character_prompt(self, parsed: ParsedRequirement, style_profile: Optional[dict] = None) -> str:
        parts = []
        if parsed.name:
            parts.append(parsed.name)

        if parsed.view:
            parts.append(f"{parsed.view} view")

        action = parsed.action
        is_sl = self._is_slime(parsed)
        if is_sl and action and action.lower() in ("walk", "walking", "行走"):
            action = "bouncing"

        if action:
            if is_sl and action == "bouncing":
                parts.append("idle bouncing pose")
            else:
                parts.append(f"{action} pose")

        if not parts:
            parts.append(parsed.subject)
        parts.append("2D game sprite")

        if is_sl:
            parts.append("round blob body")
            parts.append("simple face")
            parts.append("readable silhouette")
            parts.append("single enemy sprite")
            art_style = style_profile.get("art_style", "") if style_profile else ""
            if "pixel" in art_style:
                parts.append("pixelated blob shape")
                parts.append("hard pixel outline")
                parts.append("no smooth 3D shading")

        if parsed.appearance:
            parts.append(parsed.appearance)
        if parsed.weapon:
            parts.append(f"holding {parsed.weapon}")
        return ", ".join(parts)

    def _build_item_prompt(self, parsed: ParsedRequirement) -> str:
        parts = []
        if parsed.item_category:
            parts.append(parsed.item_category)
        if parsed.name:
            parts.append(parsed.name)
        if not parts:
            parts.append(parsed.subject)
        parts.append("game item")
        if parsed.appearance:
            parts.append(parsed.appearance)
        return ", ".join(parts)

    def _build_tile_prompt(self, parsed: ParsedRequirement) -> str:
        parts = []
        if parsed.tile_type:
            parts.append(parsed.tile_type)
        if parsed.name:
            parts.append(parsed.name)
        if not parts:
            parts.append(parsed.subject)
        parts.append("2D game tile")
        if parsed.material:
            parts.append(parsed.material)
        if parsed.seamless == "true":
            parts.append("seamless repeatable")
        return ", ".join(parts)

    def _build_ui_icon_prompt(self, parsed: ParsedRequirement) -> str:
        parts = []
        if parsed.icon_purpose:
            parts.append(parsed.icon_purpose)
        if parsed.name:
            parts.append(parsed.name)
        if not parts:
            parts.append(parsed.subject)
        parts.append("UI icon")
        if parsed.shape and parsed.shape != "no_frame":
            parts.append(f"{parsed.shape} shape")
        if parsed.appearance:
            parts.append(parsed.appearance)
        return ", ".join(parts)

    def _build_effect_prompt(self, parsed: ParsedRequirement) -> str:
        parts = []
        if parsed.effect_type:
            parts.append(parsed.effect_type)
        if parsed.name:
            parts.append(parsed.name)
        if not parts:
            parts.append(parsed.subject)
        parts.append("2D game VFX")
        if parsed.motion_feeling:
            parts.append(f"{parsed.motion_feeling} motion")
        return ", ".join(parts)

    def _get_asset_type_rules(self, parsed: ParsedRequirement) -> str:
        asset_type = parsed.asset_type or AssetType.CHARACTER
        base_rules = ASSET_TYPE_RULES.get(asset_type, ASSET_TYPE_RULES[AssetType.PROP])

        if asset_type == AssetType.TILE and parsed.seamless == "true":
            if "seamless" not in base_rules.lower():
                base_rules = base_rules + ", seamless repeatable, edge-matchable"

        return base_rules

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
