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
    SYSTEM_PROMPT = """You are a game asset requirement parser. Extract structured parameters from user input.
Return ONLY a JSON object with these fields:
- subject: the main object/person/item being drawn (string)
- style_hint: any style keywords mentioned (string)
- direction: one of "front", "back", "left", "right", or null
- background: the desired background ("transparent", "white", "black", or null)
- usage: one of "player_sprite", "enemy_sprite", "npc_sprite", "ui_element", "environment", "prop", or null

Keep subject short, max 20 words. Do not include markdown or explanation."""

    def parse(self, input_data: ParseRequirementInput) -> ParsedRequirement:
        settings = get_settings()

        result = ParsedRequirement(
            asset_type=input_data.asset_type,
            size=input_data.size,
        )

        extra = input_data.extra_params or {}
        if extra.get("direction"):
            result.direction = extra["direction"]
        if extra.get("background"):
            result.background = extra["background"]
        if extra.get("usage"):
            result.usage = extra["usage"]

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
                max_tokens=200,
            )
            raw = response.choices[0].message.content.strip()
            parsed = json.loads(raw)
            result.subject = parsed.get("subject", input_data.user_input[:50])
            result.style_hint = parsed.get("style_hint", "")
            if not result.direction:
                result.direction = parsed.get("direction")
            if not result.background:
                result.background = parsed.get("background")
            if not result.usage:
                result.usage = parsed.get("usage")
        except Exception:
            result.subject = input_data.user_input[:50]
            result.style_hint = ""
            if not result.direction:
                result.direction = "front"
            if not result.background:
                result.background = "transparent"
            if not result.usage:
                result.usage = "player_sprite"

        return result
