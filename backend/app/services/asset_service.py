# Asset management service
from typing import Optional

from ..domain.entities.asset import Asset
from ..repositories.asset_repository import AssetRepository
from ..storage.file_storage import FileStorage


class AssetService:
    def __init__(self, asset_repo: AssetRepository, file_storage: FileStorage):
        self.repo = asset_repo
        self.file_storage = file_storage

    def get_asset(self, asset_id: str) -> Optional[Asset]:
        return self.repo.get_by_id(asset_id)

    def list_by_project(self, project_id: str) -> list[Asset]:
        return self.repo.list_by_project_id(project_id)

    def save_asset(self, asset: Asset) -> Asset:
        return self.repo.create(asset)

    def delete_asset(self, asset_id: str) -> bool:
        asset = self.repo.get_by_id(asset_id)
        if asset is None:
            return False
        self.file_storage.delete(asset.file_path)
        return self.repo.delete(asset_id)

    def read_file(self, file_path: str) -> bytes:
        return self.file_storage.read(file_path)
