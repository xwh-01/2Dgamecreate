# Style profile management API endpoints
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...dependencies import get_style_service
from ...domain.enums.art_style import ArtStyle
from ...domain.enums.view_type import ViewType
from ...services.style_service import StyleService

router = APIRouter(prefix="/api/projects/{project_id}/style", tags=["styles"])


class StyleCreateBody(BaseModel):
    art_style: str
    view_type: str
    color_palette: Optional[str] = None
    default_size: Optional[str] = None
    prompt_rules: Optional[str] = None
    negative_prompt_rules: Optional[str] = None


class StyleUpdateBody(BaseModel):
    art_style: Optional[str] = None
    view_type: Optional[str] = None
    color_palette: Optional[str] = None
    default_size: Optional[str] = None
    prompt_rules: Optional[str] = None
    negative_prompt_rules: Optional[str] = None


STYLE_MAP = {
    "pixel_art": ArtStyle.PIXEL,
    "cartoon": ArtStyle.FLAT,
    "hand_drawn": ArtStyle.HAND_DRAWN,
}
VIEW_MAP = {
    "top_down": ViewType.TOP_DOWN,
    "side_view": ViewType.SIDE_SCROLLER,
    "isometric": ViewType.ISOMETRIC,
}


@router.post("")
def create_style(project_id: str, body: StyleCreateBody, service: StyleService = Depends(get_style_service)):
    art_style = STYLE_MAP.get(body.art_style, ArtStyle.PIXEL)
    view_type = VIEW_MAP.get(body.view_type, ViewType.TOP_DOWN)
    style = service.create_style(
        project_id=project_id,
        art_style=art_style,
        view_type=view_type,
        color_palette=body.color_palette,
        default_size=body.default_size,
        prompt_rules=body.prompt_rules,
        negative_prompt_rules=body.negative_prompt_rules,
    )
    return {
        "success": True,
        "style": {
            "id": style.id,
            "project_id": style.project_id,
            "art_style": style.art_style.value,
            "view_type": style.view_type.value,
            "color_palette": style.color_palette,
            "default_size": style.default_size,
            "prompt_rules": style.prompt_rules,
            "negative_prompt_rules": style.negative_prompt_rules,
        },
    }


@router.get("")
def get_style(project_id: str, service: StyleService = Depends(get_style_service)):
    styles = service.list_by_project(project_id)
    project = None
    from ...dependencies import get_project_service
    project = get_project_service().get_project(project_id)

    style = None
    if styles:
        style = styles[-1]
        return {
            "success": True,
            "style": {
                "id": style.id,
                "project_id": style.project_id,
                "art_style": style.art_style.value,
                "view_type": style.view_type.value,
                "color_palette": style.color_palette,
                "default_size": style.default_size,
                "prompt_rules": style.prompt_rules,
                "negative_prompt_rules": style.negative_prompt_rules,
            },
        }
    return {"success": True, "style": None}


@router.put("")
def update_style(project_id: str, body: StyleUpdateBody, service: StyleService = Depends(get_style_service)):
    styles = service.list_by_project(project_id)
    if not styles:
        return {"success": False, "error": "No style configured yet"}
    style = styles[-1]
    data = {}
    if body.art_style is not None:
        data["art_style"] = STYLE_MAP.get(body.art_style, ArtStyle.PIXEL).value
    if body.view_type is not None:
        data["view_type"] = VIEW_MAP.get(body.view_type, ViewType.TOP_DOWN).value
    if body.color_palette is not None:
        data["color_palette"] = body.color_palette
    if body.default_size is not None:
        data["default_size"] = body.default_size
    if body.prompt_rules is not None:
        data["prompt_rules"] = body.prompt_rules
    if body.negative_prompt_rules is not None:
        data["negative_prompt_rules"] = body.negative_prompt_rules
    updated = service.update_style(style.id, data)
    if updated is None:
        return {"success": False, "error": "Update failed"}
    return {"success": True, "style": {"id": updated.id}}
