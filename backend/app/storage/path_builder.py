# Storage path construction utility
from ..domain.enums.asset_type import AssetType


class PathBuilder:
    ROOT_DIR = "generated_assets"

    ASSET_TYPE_DIR: dict[AssetType, str] = {
        AssetType.CHARACTER: "characters",
        AssetType.ENEMY: "enemies",
        AssetType.PROP: "items",
        AssetType.TILE: "tiles",
        AssetType.UI_ICON: "ui_icons",
        AssetType.EFFECT: "effects",
    }

    def build_project_dir(self, project_id: str) -> str:
        return f"project_{project_id}"

    def build_asset_path(self, project_id: str, asset_type: AssetType, filename: str) -> str:
        dir_name = self.ASSET_TYPE_DIR.get(asset_type, "assets")
        return f"{self.ROOT_DIR}/project_{project_id}/{dir_name}/{filename}"

    def build_export_path(self, project_id: str, filename: str) -> str:
        return f"{self.ROOT_DIR}/project_{project_id}/exports/{filename}"

    def build_metadata_path(self, project_id: str) -> str:
        return f"{self.ROOT_DIR}/project_{project_id}/metadata"

    def build_history_path(self, project_id: str) -> str:
        return f"{self.ROOT_DIR}/project_{project_id}/history.json"
