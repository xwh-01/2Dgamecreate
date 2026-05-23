# Asset data access layer
from typing import Optional

from ..db.session import get_session
from ..domain.entities.asset import Asset
from ..utils.time import utcnow


class AssetRepository:
    def get_by_id(self, asset_id: str) -> Optional[Asset]:
        data = get_session().assets.get(asset_id)
        if data is None:
            return None
        return Asset(**data)

    def list_by_project_id(self, project_id: str) -> list[Asset]:
        items = get_session().assets.list_by("project_id", project_id)
        return sorted(
            [Asset(**item) for item in items],
            key=lambda a: a.created_at if a.created_at else utcnow(),
            reverse=True,
        )

    def create(self, asset: Asset) -> Asset:
        asset.created_at = utcnow()
        asset.updated_at = utcnow()
        get_session().assets.set(asset.id, {
            "id": asset.id,
            "project_id": asset.project_id,
            "task_id": asset.task_id,
            "name": asset.name,
            "asset_type": asset.asset_type.value,
            "file_path": asset.file_path,
            "preview_url": asset.preview_url,
            "width": asset.width,
            "height": asset.height,
            "format": asset.format,
            "transparent": asset.transparent,
            "metadata": asset.metadata,
            "created_at": asset.created_at.isoformat(),
            "updated_at": asset.updated_at.isoformat(),
        })
        return asset

    def update(self, asset_id: str, data_dict: dict) -> Optional[Asset]:
        existing = get_session().assets.get(asset_id)
        if existing is None:
            return None
        existing.update(data_dict)
        existing["updated_at"] = utcnow().isoformat()
        get_session().assets.set(asset_id, existing)
        return Asset(**existing)

    def delete(self, asset_id: str) -> bool:
        return get_session().assets.delete(asset_id)
