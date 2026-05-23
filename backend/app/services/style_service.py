# Style profile business logic service
from typing import Optional

from ..domain.entities.style_profile import StyleProfile
from ..repositories.style_repository import StyleRepository


class StyleService:
    def __init__(self, style_repo: StyleRepository):
        self.repo = style_repo

    def create_style(self, style_profile: StyleProfile) -> StyleProfile:
        raise NotImplementedError

    def get_style(self, style_id: str) -> Optional[StyleProfile]:
        raise NotImplementedError

    def list_by_project(self, project_id: str) -> list[StyleProfile]:
        raise NotImplementedError

    def update_style(self, style_id: str, data: dict) -> Optional[StyleProfile]:
        raise NotImplementedError

    def delete_style(self, style_id: str) -> bool:
        raise NotImplementedError
