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


CHARACTER_TEMPLATE = (
    "single subject only, {view}{pose}{emotion}{appearance}{weapon}"
    "full body from head to toe, centered in frame, "
    "transparent alpha background, no background scene, "
    "subject occupies {canvas_fill} of canvas, "
    "no white rectangle, no white box, no border, no frame, "
    "clean readable silhouette, game character sprite, "
    "2D game art style, {complexity} detail level, "
    "{body_ratio}{color_palette}{outline_style}"
    "ready for Unity Godot 2D sprite import"
)

ENEMY_TEMPLATE = (
    "single subject only, {view}{pose}{emotion}{appearance}{weapon}"
    "full body from head to toe, centered in frame, "
    "transparent alpha background, no background scene, "
    "subject occupies {canvas_fill} of canvas, "
    "no white rectangle, no white box, no border, no frame, "
    "clean readable silhouette, game enemy sprite, "
    "2D game art style, {complexity} detail level, "
    "{body_ratio}{color_palette}{outline_style}"
    "ready for Unity Godot 2D sprite import"
)

PROP_TEMPLATE = (
    "single item only, {view}{name}{appearance}{item_category}"
    "centered in frame, transparent alpha background, "
    "no background scene, no shadow on ground, "
    "subject occupies {canvas_fill} of canvas, "
    "clean readable silhouette, game item prop, "
    "2D game art style, {complexity} detail level, "
    "{color_palette}{outline_style}"
    "inventory-ready icon"
)

TILE_TEMPLATE = (
    "single tile texture, {view}{name}{tile_type}{material}"
    "top-down orthographic view, no perspective distortion, "
    "edge-matchable pattern, {seamless} "
    "2D game tile map texture, {complexity} detail level, "
    "{color_palette}{outline_style}"
    "ready for tile-based 2D game engine"
)

UI_ICON_TEMPLATE = (
    "single UI icon, {name}{icon_purpose}{appearance}{shape}"
    "centered in frame, transparent alpha background, "
    "high contrast, simple readable shape, "
    "subject occupies {canvas_fill} of canvas, "
    "clean minimal design, 2D game interface element, "
    "{color_palette}{outline_style}"
    "ready for Unity Godot UI sprite import"
)

EFFECT_TEMPLATE = (
    "single VFX sprite frame, {name}{effect_type}{motion_feeling}"
    "centered in frame, transparent alpha background, "
    "high contrast, visible against dark and light game backgrounds, "
    "subject occupies {canvas_fill} of canvas, "
    "2D game visual effect, particle or energy style, "
    "{color_palette}{outline_style}"
    "game-ready sprite sheet frame"
)


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

DEFAULT_NEGATIVE = (
    "text, watermark, logo, signature, artist name, "
    "white background, white square, white rectangle, white box, white frame, "
    "border, frame, cropped body, partial body, cut off body, "
    "tiny character, small subject, far away, zoomed out, "
    "multiple characters, multiple subjects, group, crowd, "
    "environment background, complex scene, landscape, room, scenery, "
    "realistic photo, realistic render, 3D render, 3d model, "
    "plastic toy, toy-like rendering, smooth gradient, soft realistic lighting, "
    "realistic texture, ground shadow, floating gray background, fuzzy edges, "
    "blurry, noisy background, messy details, extra limbs, six fingers"
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
        pkg.negative_prompt = self._get_negative_prompt(style_profile, parsed)
        return pkg

    def _is_slime(self, parsed: ParsedRequirement) -> bool:
        if parsed.asset_type != AssetType.ENEMY:
            return False
        text = (parsed.subject + " " + (parsed.name or "") + " " + (parsed.appearance or "")).lower()
        return any(kw in text for kw in ("slime", "slime", "圆滚滚", "slime enemy", "blob"))

    def _replace_vars(self, template: str, vars: dict) -> str:
        result = template
        for key, value in vars.items():
            placeholder = "{" + key + "}"
            if value:
                result = result.replace(placeholder, str(value) + " ")
            else:
                result = result.replace(placeholder, "")
        return " ".join(result.split())

    def _build_character_vars(self, parsed: ParsedRequirement) -> dict:
        name = parsed.name or parsed.subject or ""
        view = f"{parsed.view} view, " if parsed.view else "front view, "
        pose = f"{parsed.pose} pose, " if parsed.pose else ""
        emotion = f"{parsed.emotion} expression, " if parsed.emotion else ""
        appearance = f"{parsed.appearance}, " if parsed.appearance else ""
        weapon = f"holding {parsed.weapon}, " if parsed.weapon else ""
        canvas_fill = parsed.canvas_fill or "75%"
        complexity = parsed.complexity or "medium"
        body_ratio = f"{parsed.body_ratio} proportion, " if parsed.body_ratio else ""
        color_palette = f"{parsed.color_palette} palette, " if parsed.color_palette else ""
        outline_style = f"{parsed.outline_style} outline, " if parsed.outline_style else "clean outline, "
        return {
            "name": name,
            "view": view,
            "pose": pose,
            "emotion": emotion,
            "appearance": appearance,
            "weapon": weapon,
            "canvas_fill": canvas_fill,
            "complexity": complexity,
            "body_ratio": body_ratio,
            "color_palette": color_palette,
            "outline_style": outline_style,
        }

    def _build_prop_vars(self, parsed: ParsedRequirement) -> dict:
        name = parsed.name or parsed.subject or ""
        item_category = f"{parsed.item_category}, " if parsed.item_category else ""
        appearance = f"{parsed.appearance}, " if parsed.appearance else ""
        view = f"{parsed.view} view, " if parsed.view else ""
        canvas_fill = parsed.canvas_fill or "75%"
        complexity = parsed.complexity or "medium"
        color_palette = f"{parsed.color_palette} palette, " if parsed.color_palette else ""
        outline_style = f"{parsed.outline_style} outline, " if parsed.outline_style else "clean outline, "
        return {
            "name": name,
            "item_category": item_category,
            "appearance": appearance,
            "view": view,
            "canvas_fill": canvas_fill,
            "complexity": complexity,
            "color_palette": color_palette,
            "outline_style": outline_style,
        }

    def _build_tile_vars(self, parsed: ParsedRequirement) -> dict:
        name = parsed.name or parsed.subject or ""
        tile_type = f"{parsed.tile_type}, " if parsed.tile_type else ""
        material = f"{parsed.material} material, " if parsed.material else ""
        view = "top-down view, "
        seamless = "seamless repeatable, " if parsed.seamless == "true" else ""
        complexity = parsed.complexity or "medium"
        color_palette = f"{parsed.color_palette} palette, " if parsed.color_palette else ""
        outline_style = f"{parsed.outline_style} outline, " if parsed.outline_style else ""
        return {
            "name": name,
            "tile_type": tile_type,
            "material": material,
            "view": view,
            "seamless": seamless,
            "complexity": complexity,
            "color_palette": color_palette,
            "outline_style": outline_style,
        }

    def _build_ui_icon_vars(self, parsed: ParsedRequirement) -> dict:
        name = parsed.name or parsed.subject or ""
        icon_purpose = f"{parsed.icon_purpose}, " if parsed.icon_purpose else ""
        appearance = f"{parsed.appearance}, " if parsed.appearance else ""
        shape = f"{parsed.shape} shape, " if parsed.shape and parsed.shape != "no_frame" else ""
        canvas_fill = parsed.canvas_fill or "75%"
        color_palette = f"{parsed.color_palette} palette, " if parsed.color_palette else ""
        outline_style = f"{parsed.outline_style} outline, " if parsed.outline_style else "clean outline, "
        return {
            "name": name,
            "icon_purpose": icon_purpose,
            "appearance": appearance,
            "shape": shape,
            "canvas_fill": canvas_fill,
            "color_palette": color_palette,
            "outline_style": outline_style,
        }

    def _build_effect_vars(self, parsed: ParsedRequirement) -> dict:
        name = parsed.name or parsed.subject or ""
        effect_type = f"{parsed.effect_type}, " if parsed.effect_type else ""
        motion_feeling = f"{parsed.motion_feeling} motion, " if parsed.motion_feeling else ""
        canvas_fill = parsed.canvas_fill or "75%"
        color_palette = f"{parsed.color_palette} palette, " if parsed.color_palette else ""
        outline_style = f"{parsed.outline_style} outline, " if parsed.outline_style else ""
        return {
            "name": name,
            "effect_type": effect_type,
            "motion_feeling": motion_feeling,
            "canvas_fill": canvas_fill,
            "color_palette": color_palette,
            "outline_style": outline_style,
        }

    def _build_base_prompt(self, parsed: ParsedRequirement, style_profile: Optional[dict] = None) -> str:
        asset_type = parsed.asset_type

        if asset_type in (AssetType.CHARACTER, AssetType.ENEMY):
            template = CHARACTER_TEMPLATE if asset_type == AssetType.CHARACTER else ENEMY_TEMPLATE
            is_sl = self._is_slime(parsed)
            vars_ = self._build_character_vars(parsed)
            if is_sl:
                vars_["appearance"] = "round blob body, simple face, "
                if "idle" in (vars_.get("pose", "")).lower():
                    vars_["pose"] = "idle bouncing pose, "
            return self._replace_vars(template, vars_)
        if asset_type == AssetType.PROP:
            return self._replace_vars(PROP_TEMPLATE, self._build_prop_vars(parsed))
        if asset_type == AssetType.TILE:
            return self._replace_vars(TILE_TEMPLATE, self._build_tile_vars(parsed))
        if asset_type == AssetType.UI_ICON:
            return self._replace_vars(UI_ICON_TEMPLATE, self._build_ui_icon_vars(parsed))
        if asset_type == AssetType.EFFECT:
            return self._replace_vars(EFFECT_TEMPLATE, self._build_effect_vars(parsed))

        parts = [parsed.subject]
        if parsed.view:
            parts.append(f"{parsed.view} view")
        if parsed.direction:
            parts.append(f"facing {parsed.direction}")
        return " ".join(parts)

    def _get_asset_type_rules(self, parsed: ParsedRequirement) -> str:
        asset_type = parsed.asset_type or AssetType.CHARACTER
        if asset_type in (AssetType.CHARACTER, AssetType.ENEMY):
            return (
                "single 2D game character sprite, full body, centered, "
                "transparent background, clean readable silhouette, "
                "suitable for Unity Godot 2D game, game-ready character, "
                "no background clutter, isolated on transparent"
            )
        if asset_type == AssetType.PROP:
            return (
                "single 2D game item icon, centered, transparent background, "
                "no text, clean readable silhouette, game prop, inventory item, "
                "isolated on transparent"
            )
        if asset_type == AssetType.TILE:
            base = (
                "2D game tile texture, top-down view, edge-matchable, "
                "no perspective distortion, suitable for tile map, game-ready tile"
            )
            if parsed.seamless == "true":
                base = base + ", seamless repeatable, edge-matchable"
            return base
        if asset_type == AssetType.UI_ICON:
            return (
                "clean 2D game UI icon, centered, transparent background, "
                "high contrast, simple readable shape, clean design, "
                "game interface element"
            )
        if asset_type == AssetType.EFFECT:
            return (
                "2D game VFX sprite, transparent background, centered, "
                "high contrast, readable in game, particle or energy effect style, "
                "game visual effect frame, isolated on transparent"
            )
        return ""

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
        bg = parsed.background or "transparent"
        if bg == "transparent":
            parts.append("transparent background, alpha channel")
        else:
            parts.append(f"{bg} background")
        parts.append("game-ready sprite sheet compatible")
        return ", ".join(parts)

    def _get_engine_rules(self) -> str:
        return "pixel perfect, centered pivot, no shadow, isolated on transparent, ready for Unity Godot sprite import"

    def _get_negative_prompt(self, style_profile: Optional[dict], parsed: ParsedRequirement) -> str:
        neg = DEFAULT_NEGATIVE
        for el in parsed.forbidden_elements:
            if el and el not in neg:
                neg = f"{neg}, {el}"
        if style_profile and style_profile.get("negative_prompt_rules"):
            neg = f"{neg}, {style_profile['negative_prompt_rules']}"
        return neg
