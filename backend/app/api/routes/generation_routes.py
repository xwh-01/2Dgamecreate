# Asset generation trigger and management API endpoints
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...dependencies import get_generation_service
from ...domain.enums.asset_type import AssetType
from ...schemas.generation_schema import GenerationCreateRequest
from ...services.generation_service import GenerationService

router = APIRouter(tags=["generations"])


def _translate_error(error_message: str) -> str:
    if not error_message:
        return "未知错误"
    msg = error_message.lower()
    if "image provider is not configured" in msg or "not configured" in msg:
        return "未配置图片生成 API Key，请在 .env 文件中设置 IMAGE_API_KEY"
    if "tongyi wanxiang" in msg:
        return "通义万象图片生成服务调用失败，请检查 API Key 是否正确"
    if "openai" in msg and ("api" in msg or "auth" in msg):
        return "OpenAI 服务认证失败，请检查 API Key 是否正确"
    if "image generation failed" in msg or "generation failed" in msg:
        return "图片生成服务调用失败，请稍后重试"
    if "task not found" in msg:
        return "生成任务不存在"
    if "project not found" in msg:
        return "项目不存在，请先创建项目"
    if "style profile" in msg or "style_profile" in msg:
        return "画风配置不存在，请先在画风配置标签页中配置画风"
    if "rate" in msg or "quota" in msg or "billing" in msg:
        return "API 额度不足或已达速率限制，请稍后重试"
    if "content" in msg or "safety" in msg or "policy" in msg:
        return "内容被安全策略拦截，请修改描述后重试"
    if "unsupported" in msg:
        return "不支持的图片生成服务商，请检查 IMAGE_PROVIDER 配置"
    return error_message[:200] if len(error_message) > 200 else error_message


class ExtraParamsModel(BaseModel):
    direction: Optional[str] = None
    background: Optional[str] = None
    usage: Optional[str] = None
    # structured fields per asset type
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


class GenerationCreateBody(BaseModel):
    project_id: str
    asset_type: str
    description: str
    size: Optional[str] = None
    quantity: int = 1
    extra_params: Optional[ExtraParamsModel] = None


ASSET_TYPE_MAP = {
    "character": AssetType.CHARACTER,
    "enemy": AssetType.ENEMY,
    "item": AssetType.PROP,
    "prop": AssetType.PROP,
    "tile": AssetType.TILE,
    "ui_icon": AssetType.UI_ICON,
    "effect": AssetType.EFFECT,
}


@router.post("/api/generations")
def create_generation(body: GenerationCreateBody, service: GenerationService = Depends(get_generation_service)):
    asset_type = ASSET_TYPE_MAP.get(body.asset_type)
    if asset_type is None:
        known = ", ".join(sorted(ASSET_TYPE_MAP.keys()))
        return {
            "success": False,
            "task": {
                "id": "",
                "status": "failed",
                "asset_id": None,
                "preview_url": None,
                "download_url": None,
                "error_message": f"不支持的素材类型: {body.asset_type}，当前支持: {known}",
            },
        }
    from ...schemas.generation_schema import ExtraParams

    extra = None
    if body.extra_params:
        extra = ExtraParams(
            direction=body.extra_params.direction,
            background=body.extra_params.background,
            usage=body.extra_params.usage,
            name=body.extra_params.name,
            view=body.extra_params.view,
            action=body.extra_params.action,
            appearance=body.extra_params.appearance,
            weapon=body.extra_params.weapon,
            item_category=body.extra_params.item_category,
            tile_type=body.extra_params.tile_type,
            material=body.extra_params.material,
            seamless=body.extra_params.seamless,
            icon_purpose=body.extra_params.icon_purpose,
            shape=body.extra_params.shape,
            effect_type=body.extra_params.effect_type,
            motion_feeling=body.extra_params.motion_feeling,
        )

    request = GenerationCreateRequest(
        project_id=body.project_id,
        asset_type=asset_type,
        description=body.description,
        size=body.size,
        quantity=body.quantity,
        extra_params=extra,
    )

    task = service.create_task(request)

    try:
        ctx = service.run_task(task.id)
    except Exception as e:
        raw_error = str(e)
        return {
            "success": False,
            "task": {
                "id": task.id,
                "status": "failed",
                "asset_id": None,
                "preview_url": None,
                "download_url": None,
                "error_message": _translate_error(raw_error),
            },
        }

    if ctx.asset_record and ctx.asset_record.preview_url:
        preview_url = ctx.asset_record.preview_url
        download_url = f"/api/download/{ctx.asset_record.id}"
        return {
            "success": True,
            "task": {
                "id": task.id,
                "status": "succeeded",
                "asset_id": ctx.asset_record.id,
                "preview_url": preview_url,
                "download_url": download_url,
                "error_message": None,
            },
        }
    else:
        raw_error = ctx.error_message or "未知错误"
        return {
            "success": False,
            "task": {
                "id": task.id,
                "status": "failed",
                "asset_id": None,
                "preview_url": None,
                "download_url": None,
                "error_message": _translate_error(raw_error),
            },
        }


@router.get("/api/generations/{task_id}")
def get_generation(task_id: str, service: GenerationService = Depends(get_generation_service)):
    task = service.get_task(task_id)
    if task is None:
        return {"success": False, "error": "Task not found"}

    preview_url = None
    download_url = None
    if task.result_asset_id:
        from ...dependencies import get_asset_service
        asset = get_asset_service().get_asset(task.result_asset_id)
        if asset:
            preview_url = asset.preview_url
            download_url = f"/api/download/{asset.id}"

    return {
        "success": True,
        "task": {
            "id": task.id,
            "status": task.status.value,
            "asset_id": task.result_asset_id,
            "preview_url": preview_url,
            "download_url": download_url,
            "error_message": task.error_message,
        },
    }


@router.get("/api/projects/{project_id}/generations")
def list_project_generations(project_id: str, service: GenerationService = Depends(get_generation_service)):
    tasks = service.list_by_project(project_id)
    return {
        "success": True,
        "generations": [
            {
                "id": t.id,
                "status": t.status.value,
                "asset_type": t.asset_type.value,
                "user_input": t.user_input,
                "result_asset_id": t.result_asset_id,
                "error_message": t.error_message,
                "created_at": t.created_at.isoformat() if t.created_at else "",
            }
            for t in sorted(tasks, key=lambda x: x.created_at or "", reverse=True)
        ],
    }
