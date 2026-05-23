# Asset management service
from typing import Optional

from ..domain.entities.asset import Asset
from ..repositories.asset_repository import AssetRepository


class AssetService:
    def __init__(self, asset_repo: AssetRepository):
        self.repo = asset_repo

    def get_asset(self, asset_id: str) -> Optional[Asset]:
        raise NotImplementedError

    def list_by_project(self, project_id: str) -> list[Asset]:
        raise NotImplementedError

    def save_asset(self, asset: Asset) -> Asset:
        raise NotImplementedError

    def delete_asset(self, asset_id: str) -> bool:
        raise NotImplementedError
