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
            ("Subject", self.base_prompt),
            ("Composition", self.asset_type_rules),
            ("Style", self.style_profile_rules),
            ("Technical", self.technical_rules),
            ("Negative constraints", self.negative_prompt),
            ("Engine compatibility", self.engine_compatibility_rules),
        ]
        return "\n".join(f"{title}: {body}" for title, body in sections if body)

    def to_full_negative_prompt(self) -> str:
        return self.negative_prompt


STYLE_RULES = {
    "pixel_art": (
        "pixel art sprite, crisp hard pixel edges, limited palette, no anti-aliasing, "
        "readable at small sizes, flat pixel shading"
    ),
    "cartoon": (
        "stylized 2D cartoon game art, clean outline, flat or cel shading, simple shapes, "
        "no toy-like 3D render"
    ),
    "hand_drawn": (
        "hand drawn 2D game art, expressive line work, readable silhouette, no 3D render"
    ),
}

DEFAULT_NEGATIVE = [
    "text",
    "watermark",
    "logo",
    "signature",
    "artist name",
    "white background",
    "white square",
    "white rectangle",
    "white box",
    "border",
    "frame",
    "cropped body",
    "cut off body",
    "tiny subject",
    "multiple subjects",
    "group",
    "crowd",
    "environment background",
    "complex scene",
    "landscape",
    "room",
    "realistic photo",
    "3D render",
    "3d model",
    "plastic toy",
    "smooth gradient",
    "soft realistic lighting",
    "ground shadow",
    "blurry",
    "messy details",
]


class PromptBuilder:
    def build(
        self,
        parsed: ParsedRequirement,
        style_profile: Optional[dict] = None,
    ) -> PromptPackage:
        pkg = PromptPackage()
        pkg.base_prompt = self._build_subject_section(parsed)
        pkg.asset_type_rules = self._build_composition_section(parsed)
        pkg.style_profile_rules = self._build_style_section(parsed, style_profile)
        pkg.technical_rules = self._build_technical_section(parsed)
        pkg.engine_compatibility_rules = self._get_engine_rules(parsed)
        pkg.negative_prompt = self._get_negative_prompt(style_profile, parsed)
        return pkg

    def _build_subject_section(self, parsed: ParsedRequirement) -> str:
        asset_type = parsed.asset_type or AssetType.CHARACTER
        values = {
            "asset_type": self._asset_type_label(asset_type),
            "name": parsed.name,
            "subject": parsed.subject,
            "appearance": parsed.appearance,
            "item_category": parsed.item_category,
            "tile_type": parsed.tile_type,
            "material": parsed.material,
            "icon_purpose": parsed.icon_purpose,
            "effect_type": parsed.effect_type,
            "weapon": f"holding {parsed.weapon}" if parsed.weapon else None,
            "emotion": f"{parsed.emotion} expression" if parsed.emotion else None,
            "pose": self._pose_text(parsed),
            "action": f"action: {parsed.action}" if parsed.action else None,
            "animation_frame": parsed.animation_frame,
            "motion_feeling": (
                f"{parsed.motion_feeling} motion" if parsed.motion_feeling else None
            ),
        }

        if asset_type == AssetType.ENEMY:
            values["role"] = (
                "hostile creature, enemy sprite, attack-ready game opponent"
            )
        elif asset_type == AssetType.CHARACTER:
            values["role"] = "player or NPC character sprite"
        elif asset_type == AssetType.PROP:
            values["role"] = "single usable game item or prop"
        elif asset_type == AssetType.TILE:
            values["role"] = "single 2D tile texture"
        elif asset_type == AssetType.UI_ICON:
            values["role"] = "single game UI icon"
        elif asset_type == AssetType.EFFECT:
            values["role"] = "single visual effect sprite frame"

        if self._is_slime_enemy(parsed):
            values["role"] = "slime enemy sprite, round blob body, simple face"
            if not parsed.pose and not parsed.action:
                values["pose"] = "idle bouncing pose"

        return self._join_values(values)

    def _build_composition_section(self, parsed: ParsedRequirement) -> str:
        asset_type = parsed.asset_type or AssetType.CHARACTER
        rules = [
            "single asset only",
            "centered in frame",
            "isolated on transparent background",
            "no complex scene",
        ]

        if asset_type == AssetType.ENEMY:
            rules.extend(
                [
                    "full body from head to toe",
                    "hostile creature",
                    "enemy sprite",
                    "readable silhouette",
                    "attack-ready pose",
                    "suitable for RPG, platformer, or roguelike game",
                ]
            )
            if self._is_slime_enemy(parsed):
                rules.append("round blob silhouette")
        elif asset_type == AssetType.CHARACTER:
            rules.extend(
                [
                    "full body from head to toe",
                    "game character sprite",
                    "readable silhouette",
                ]
            )
        elif asset_type == AssetType.PROP:
            rules.extend(["single item only", "inventory-ready item icon"])
        elif asset_type == AssetType.TILE:
            rules.extend(["top-down orthographic tile", "edge-matchable pattern"])
            if self._is_true(parsed.seamless):
                rules.append("seamless repeatable texture")
        elif asset_type == AssetType.UI_ICON:
            rules.extend(["high contrast icon", "simple readable shape"])
            if parsed.shape and parsed.shape != "no_frame":
                rules.append(f"{parsed.shape} icon shape")
            else:
                rules.append("no decorative frame")
        elif asset_type == AssetType.EFFECT:
            rules.extend(
                [
                    "transparent VFX element",
                    "visible on dark and light game backgrounds",
                ]
            )

        if parsed.camera_angle:
            rules.append(f"camera angle: {parsed.camera_angle}")
        if parsed.view:
            rules.append(f"view: {parsed.view}")
        if parsed.direction:
            rules.append(f"facing {parsed.direction}")
        if parsed.body_ratio:
            rules.append(f"{parsed.body_ratio} body ratio")
        if parsed.canvas_fill:
            rules.append(f"subject fills about {parsed.canvas_fill} of the canvas")

        return ", ".join(self._dedupe(rules))

    def _build_style_section(
        self, parsed: ParsedRequirement, style_profile: Optional[dict]
    ) -> str:
        parts = [
            "2D game art",
            "game-ready sprite",
            parsed.style_hint,
            f"{parsed.complexity} detail level" if parsed.complexity else None,
            f"{parsed.color_palette} color palette" if parsed.color_palette else None,
            f"{parsed.outline_style} outline" if parsed.outline_style else None,
        ]

        if style_profile:
            art_style = style_profile.get("art_style", "")
            parts.append(STYLE_RULES.get(art_style, ""))
            parts.append(style_profile.get("prompt_rules", ""))
            if style_profile.get("default_size"):
                parts.append(f"default sprite size {style_profile['default_size']}")

        asset_type = parsed.asset_type or AssetType.CHARACTER
        if asset_type in (AssetType.CHARACTER, AssetType.ENEMY):
            parts.append("clean readable silhouette")
        if asset_type == AssetType.UI_ICON:
            parts.append("simple interface-ready design")
        if asset_type == AssetType.TILE:
            parts.append("tilemap-ready texture")

        return ", ".join(self._dedupe(self._clean_list(parts)))

    def _build_technical_section(self, parsed: ParsedRequirement) -> str:
        bg = parsed.background or "transparent"
        parts = [
            parsed.size,
            "transparent background with alpha channel"
            if bg == "transparent"
            else f"{bg} background",
            "no text",
            "no watermark",
            "no white box",
            "no border or frame",
            "game-ready sprite",
            "clean alpha edges",
        ]
        if parsed.animation_frame:
            parts.append(f"animation frame: {parsed.animation_frame}")
        return ", ".join(self._dedupe(self._clean_list(parts)))

    def _get_engine_rules(self, parsed: ParsedRequirement) -> str:
        asset_type = parsed.asset_type or AssetType.CHARACTER
        parts = [
            "ready for Unity or Godot 2D import",
            "centered pivot",
            "consistent sprite scale",
            "no baked ground shadow",
        ]
        if asset_type == AssetType.TILE:
            parts.append("ready for tilemap import")
        if asset_type == AssetType.UI_ICON:
            parts.append("ready for UI atlas import")
        return ", ".join(parts)

    def _get_negative_prompt(
        self, style_profile: Optional[dict], parsed: ParsedRequirement
    ) -> str:
        items = list(DEFAULT_NEGATIVE)
        items.extend(parsed.forbidden_elements or [])
        if style_profile and style_profile.get("negative_prompt_rules"):
            items.extend(self._split_negative(style_profile["negative_prompt_rules"]))
        return ", ".join(self._dedupe(self._clean_list(items)))

    def _pose_text(self, parsed: ParsedRequirement) -> Optional[str]:
        pose = parsed.pose or parsed.action
        if parsed.asset_type == AssetType.ENEMY and not pose:
            pose = "attack-ready"
        if pose:
            return f"{pose} pose"
        return None

    def _asset_type_label(self, asset_type: AssetType) -> str:
        labels = {
            AssetType.CHARACTER: "character",
            AssetType.ENEMY: "enemy",
            AssetType.PROP: "prop",
            AssetType.TILE: "tile",
            AssetType.UI_ICON: "ui icon",
            AssetType.EFFECT: "effect",
        }
        return labels.get(asset_type, "asset")

    def _join_values(self, values: dict) -> str:
        preferred = [
            "asset_type",
            "role",
            "name",
            "subject",
            "item_category",
            "tile_type",
            "material",
            "icon_purpose",
            "effect_type",
            "appearance",
            "pose",
            "action",
            "emotion",
            "weapon",
            "motion_feeling",
            "animation_frame",
        ]
        parts = [values.get(key) for key in preferred]
        return ", ".join(self._dedupe(self._clean_list(parts)))

    def _clean_list(self, values: list) -> list[str]:
        clean = []
        for value in values:
            if value is None:
                continue
            text = str(value).strip(" ,")
            if text:
                clean.append(text)
        return clean

    def _dedupe(self, values: list[str]) -> list[str]:
        seen = set()
        result = []
        for value in values:
            key = value.lower()
            if key in seen:
                continue
            seen.add(key)
            result.append(value)
        return result

    def _split_negative(self, text: str) -> list[str]:
        return [part.strip() for part in text.split(",") if part.strip()]

    def _is_true(self, value: Optional[str]) -> bool:
        return str(value).lower() in ("1", "true", "yes", "y")

    def _is_slime_enemy(self, parsed: ParsedRequirement) -> bool:
        if parsed.asset_type != AssetType.ENEMY:
            return False
        text = " ".join(
            self._clean_list([parsed.subject, parsed.name, parsed.appearance])
        ).lower()
        return any(keyword in text for keyword in ("slime", "blob", "史莱姆"))
