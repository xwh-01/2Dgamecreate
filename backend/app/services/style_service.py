# Style profile business logic service
import uuid
from typing import Optional

from ..domain.entities.style_profile import StyleProfile
from ..domain.enums.art_style import ArtStyle
from ..domain.enums.view_type import ViewType
from ..repositories.style_repository import StyleRepository


class StyleService:
    def __init__(self, style_repo: StyleRepository):
        self.repo = style_repo

    def create_style(
        self,
        project_id: str,
        art_style: ArtStyle,
        view_type: ViewType,
        color_palette: Optional[str] = None,
        outline_style: Optional[str] = None,
        default_size: Optional[str] = None,
        prompt_rules: Optional[str] = None,
        negative_prompt_rules: Optional[str] = None,
    ) -> StyleProfile:
        style = StyleProfile(
            id=str(uuid.uuid4()),
            project_id=project_id,
            art_style=art_style,
            view_type=view_type,
            color_palette=color_palette,
            outline_style=outline_style,
            default_size=default_size,
            prompt_rules=prompt_rules,
            negative_prompt_rules=negative_prompt_rules,
        )
        result = self.repo.create(style)
        from ..repositories.project_repository import ProjectRepository
        from ..db.session import get_session

        project_repo = ProjectRepository()
        project_repo.update(project_id, {"style_profile_id": style.id})
        return result

    def get_style(self, style_id: str) -> Optional[StyleProfile]:
        return self.repo.get_by_id(style_id)

    def list_by_project(self, project_id: str) -> list[StyleProfile]:
        return self.repo.list_by_project_id(project_id)

    def update_style(self, style_id: str, data: dict) -> Optional[StyleProfile]:
        return self.repo.update(style_id, data)

    def delete_style(self, style_id: str) -> bool:
        return self.repo.delete(style_id)
