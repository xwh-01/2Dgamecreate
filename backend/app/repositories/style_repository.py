# Style profile data access layer
from typing import Optional

from ..domain.entities.style_profile import StyleProfile


class StyleRepository:
    def get_by_id(self, style_id: str) -> Optional[StyleProfile]:
        raise NotImplementedError

    def list_by_project_id(self, project_id: str) -> list[StyleProfile]:
        raise NotImplementedError

    def create(self, style_profile: StyleProfile) -> StyleProfile:
        raise NotImplementedError

    def update(self, style_id: str, data: dict) -> Optional[StyleProfile]:
        raise NotImplementedError

    def delete(self, style_id: str) -> bool:
        raise NotImplementedError
