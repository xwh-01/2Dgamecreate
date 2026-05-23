# Asset data access layer
from typing import Optional

from ..domain.entities.asset import Asset


class AssetRepository:
    def get_by_id(self, asset_id: str) -> Optional[Asset]:
        raise NotImplementedError

    def list_by_project_id(self, project_id: str) -> list[Asset]:
        raise NotImplementedError

    def create(self, asset: Asset) -> Asset:
        raise NotImplementedError

    def update(self, asset_id: str, data: dict) -> Optional[Asset]:
        raise NotImplementedError

    def delete(self, asset_id: str) -> bool:
        raise NotImplementedError
