# Style profile data access layer
from typing import Optional

from ..db.session import get_session
from ..domain.entities.style_profile import StyleProfile
from ..utils.time import utcnow


class StyleRepository:
    def get_by_id(self, style_id: str) -> Optional[StyleProfile]:
        data = get_session().styles.get(style_id)
        if data is None:
            return None
        return StyleProfile(**data)

    def list_by_project_id(self, project_id: str) -> list[StyleProfile]:
        items = get_session().styles.list_by("project_id", project_id)
        return [StyleProfile(**item) for item in items]

    def create(self, style_profile: StyleProfile) -> StyleProfile:
        style_profile.created_at = utcnow()
        style_profile.updated_at = utcnow()
        get_session().styles.set(style_profile.id, {
            "id": style_profile.id,
            "project_id": style_profile.project_id,
            "art_style": style_profile.art_style.value,
            "view_type": style_profile.view_type.value,
            "color_palette": style_profile.color_palette,
            "outline_style": style_profile.outline_style,
            "default_size": style_profile.default_size,
            "prompt_rules": style_profile.prompt_rules,
            "negative_prompt_rules": style_profile.negative_prompt_rules,
            "created_at": style_profile.created_at.isoformat(),
            "updated_at": style_profile.updated_at.isoformat(),
        })
        return style_profile

    def update(self, style_id: str, data_dict: dict) -> Optional[StyleProfile]:
        existing = get_session().styles.get(style_id)
        if existing is None:
            return None
        existing.update(data_dict)
        existing["updated_at"] = utcnow().isoformat()
        get_session().styles.set(style_id, existing)
        return StyleProfile(**existing)

    def delete(self, style_id: str) -> bool:
        return get_session().styles.delete(style_id)
