# Natural language requirement parser using AI
import json
from dataclasses import dataclass, field
from typing import Optional

from openai import OpenAI

from ..config import get_settings
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
    name: Optional[str] = None
    view: Optional[str] = None
    action: Optional[str] = None
    appearance: Optional[str] = None
    weapon: Optional[str] = None
    item_category: Optional[str] = None
    tile_type: Optional[str] = None
    material: Optional[str] = None
    seamless: Optional[str] = None
    icon_purpose: Optional[str] = None
    shape: Optional[str] = None
    effect_type: Optional[str] = None
    motion_feeling: Optional[str] = None

    pose: Optional[str] = None
    camera_angle: Optional[str] = None
    body_ratio: Optional[str] = None
    canvas_fill: Optional[str] = None
    outline_style: Optional[str] = None
    color_palette: Optional[str] = None
    emotion: Optional[str] = None
    complexity: Optional[str] = None
    animation_frame: Optional[str] = None
    forbidden_elements: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "asset_type": self.asset_type.value if self.asset_type else None,
            "subject": self.subject,
            "style_hint": self.style_hint,
            "size": self.size,
            "direction": self.direction,
            "background": self.background,
            "usage": self.usage,
            "name": self.name,
            "view": self.view,
            "action": self.action,
            "appearance": self.appearance,
            "weapon": self.weapon,
            "item_category": self.item_category,
            "tile_type": self.tile_type,
            "material": self.material,
            "seamless": self.seamless,
            "icon_purpose": self.icon_purpose,
            "shape": self.shape,
            "effect_type": self.effect_type,
            "motion_feeling": self.motion_feeling,
            "pose": self.pose,
            "camera_angle": self.camera_angle,
            "body_ratio": self.body_ratio,
            "canvas_fill": self.canvas_fill,
            "outline_style": self.outline_style,
            "color_palette": self.color_palette,
            "emotion": self.emotion,
            "complexity": self.complexity,
            "animation_frame": self.animation_frame,
            "forbidden_elements": self.forbidden_elements,
        }


class RequirementParser:
    SYSTEM_PROMPT = """You are a game asset requirement parser. Extract structured parameters from user input.
Return ONLY a JSON object with these fields:

Core fields:
- subject: the main object/person/item being drawn (string, max 20 words)
- style_hint: any style keywords mentioned (string)
- direction: one of "front", "back", "left", "right", or null
- background: desired background ("transparent" preferred for sprites, "white", "black", or null)
- usage: one of "player_sprite", "enemy_sprite", "npc_sprite", "ui_element", "environment", "prop", or null

Advanced control fields:
- pose: one of "idle", "walking", "attacking", "casting", "hurt", "dead", or null
- camera_angle: one of "front", "side", "back", "three-quarter", "top-down", or null
- body_ratio: preferred body proportion e.g. "chibi", "realistic", "1:1", "1:2", or null
- canvas_fill: how much of the canvas the subject fills: "60%", "75%", "85%", or null
- outline_style: one of "clean", "sketchy", "none", "thick", "thin", or null
- color_palette: color scheme hint e.g. "pastel", "dark", "vibrant", "monochrome", "warm", "cool", or null
- emotion: subject emotion e.g. "neutral", "angry", "happy", "sad", "fierce", "calm", or null
- complexity: level of detail: "simple", "medium", "detailed", or null
- animation_frame: hint if this is a specific animation frame e.g. "idle_1", "walk_3", or null
- forbidden_elements: array of strings, things that must NOT appear. Default to ["text", "watermark", "white background", "complex scene"] if none specified.

For sprites/characters/enemies, background default is "transparent", canvas_fill default is "75%".
Do not include markdown or explanation."""

    def parse(self, input_data: ParseRequirementInput) -> ParsedRequirement:
        settings = get_settings()

        result = ParsedRequirement(
            asset_type=input_data.asset_type,
            size=input_data.size,
        )

        extra = input_data.extra_params or {}

        result.direction = extra.get("direction")
        result.background = extra.get("background")
        result.usage = extra.get("usage")
        result.name = extra.get("name")
        result.view = extra.get("view")
        result.action = extra.get("action")
        result.appearance = extra.get("appearance")
        result.weapon = extra.get("weapon")
        result.item_category = extra.get("item_category")
        result.tile_type = extra.get("tile_type")
        result.material = extra.get("material")
        result.seamless = extra.get("seamless")
        result.icon_purpose = extra.get("icon_purpose")
        result.shape = extra.get("shape")
        result.effect_type = extra.get("effect_type")
        result.motion_feeling = extra.get("motion_feeling")

        result.pose = extra.get("pose")
        result.camera_angle = extra.get("camera_angle")
        result.body_ratio = extra.get("body_ratio")
        result.canvas_fill = extra.get("canvas_fill")
        result.outline_style = extra.get("outline_style")
        result.color_palette = extra.get("color_palette")
        result.emotion = extra.get("emotion")
        result.complexity = extra.get("complexity")
        result.animation_frame = extra.get("animation_frame")
        result.forbidden_elements = extra.get("forbidden_elements", [])

        structured_subject = self._build_subject_from_structured(
            input_data.asset_type, extra, input_data.user_input
        )

        ai_subject = ""
        ai_style_hint = ""
        dk_key = settings.deepseek_api_key

        try:
            if dk_key:
                client = OpenAI(api_key=dk_key, base_url="https://api.deepseek.com")
                model = settings.deepseek_model
            else:
                client = OpenAI(api_key=settings.image_api_key)
                model = "gpt-3.5-turbo"

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": input_data.user_input},
                ],
                temperature=0.1,
                max_tokens=500,
            )
            raw = response.choices[0].message.content.strip()
            parsed = json.loads(raw)
            ai_subject = parsed.get("subject", "")
            ai_style_hint = parsed.get("style_hint", "")

            if not result.direction:
                result.direction = parsed.get("direction")
            if not result.background:
                result.background = parsed.get("background")
            if not result.usage:
                result.usage = parsed.get("usage")

            if not result.pose:
                result.pose = parsed.get("pose")
            if not result.camera_angle:
                result.camera_angle = parsed.get("camera_angle")
            if not result.body_ratio:
                result.body_ratio = parsed.get("body_ratio")
            if not result.canvas_fill:
                result.canvas_fill = parsed.get("canvas_fill")
            if not result.outline_style:
                result.outline_style = parsed.get("outline_style")
            if not result.color_palette:
                result.color_palette = parsed.get("color_palette")
            if not result.emotion:
                result.emotion = parsed.get("emotion")
            if not result.complexity:
                result.complexity = parsed.get("complexity")
            if not result.animation_frame:
                result.animation_frame = parsed.get("animation_frame")
            if not result.forbidden_elements:
                fe = parsed.get("forbidden_elements", [])
                if isinstance(fe, list):
                    result.forbidden_elements = fe
        except Exception:
            if not result.direction:
                result.direction = "front"
            if not result.background:
                result.background = "transparent"
            if not result.usage:
                result.usage = "player_sprite"

        if not result.forbidden_elements:
            result.forbidden_elements = ["text", "watermark", "white background", "complex scene"]
        if not result.canvas_fill:
            result.canvas_fill = "75%"
        if not result.complexity:
            result.complexity = "medium"

        if structured_subject:
            result.subject = structured_subject
        elif ai_subject:
            result.subject = ai_subject
        else:
            result.subject = input_data.user_input[:50]

        result.style_hint = ai_style_hint or extra.get("style_hint", "")
        return result

    def _build_subject_from_structured(
        self,
        asset_type: Optional[AssetType],
        extra: dict,
        user_input: str,
    ) -> str:
        name = extra.get("name", "")
        appearance = extra.get("appearance", "")
        if not name and not appearance:
            return ""

        if asset_type in (AssetType.CHARACTER, AssetType.ENEMY):
            view = extra.get("view", "")
            action = extra.get("action", "")
            weapon = extra.get("weapon", "")
            emotion = extra.get("emotion", "")
            parts = [name]
            if view:
                parts.append(f"{view} view")
            if action:
                parts.append(f"{action} pose")
            if emotion:
                parts.append(f"{emotion} expression")
            if appearance:
                parts.append(appearance)
            if weapon:
                parts.append(f"holding {weapon}")
            return ", ".join(parts)

        if asset_type == AssetType.PROP:
            cat = extra.get("item_category", "")
            if cat:
                return f"{cat} {name}, {appearance}"
            return f"{name}, {appearance}"

        if asset_type == AssetType.TILE:
            tile_type = extra.get("tile_type", "")
            material = extra.get("material", "")
            seamless = extra.get("seamless", "")
            parts = []
            if tile_type:
                parts.append(tile_type)
            parts.append("tile")
            if material:
                parts.append(material)
            if seamless == "true":
                parts.append("seamless repeatable")
            return ", ".join(parts)

        if asset_type == AssetType.UI_ICON:
            purpose = extra.get("icon_purpose", "")
            shape = extra.get("shape", "")
            parts = []
            if purpose:
                parts.append(purpose)
            parts.append("icon")
            if name:
                parts.append(name)
            if shape and shape != "no_frame":
                parts.append(f"{shape} shape")
            if appearance:
                parts.append(appearance)
            return ", ".join(parts)

        if asset_type == AssetType.EFFECT:
            etype = extra.get("effect_type", "")
            motion = extra.get("motion_feeling", "")
            parts = []
            if etype:
                parts.append(etype)
            parts.append("effect")
            if name:
                parts.append(name)
            if motion:
                parts.append(f"{motion} motion")
            return ", ".join(parts)

        return ""
