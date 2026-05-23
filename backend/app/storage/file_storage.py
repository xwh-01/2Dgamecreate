# Local file system storage operations
import os

from .path_builder import PathBuilder


class FileStorage:
    def __init__(self, path_builder: PathBuilder, base_dir: str = ""):
        self.path_builder = path_builder
        self.base_dir = base_dir or os.path.join(os.path.dirname(__file__), "..", "..")

    def _full_path(self, file_path: str) -> str:
        return os.path.join(self.base_dir, file_path)

    def save(self, file_path: str, data: bytes) -> str:
        full = self._full_path(file_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as f:
            f.write(data)
        return file_path

    def read(self, file_path: str) -> bytes:
        full = self._full_path(file_path)
        if not os.path.exists(full):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(full, "rb") as f:
            return f.read()

    def delete(self, file_path: str) -> bool:
        full = self._full_path(file_path)
        if os.path.exists(full):
            os.remove(full)
            return True
        return False

    def get_url(self, file_path: str) -> str:
        return f"/assets/{file_path}"

    def ensure_type_dirs(self, project_id: str):
        project_dir = self._full_path(f"generated_assets/project_{project_id}")
        for dir_name in ["characters", "items", "tiles", "ui_icons", "effects", "metadata", "exports"]:
            os.makedirs(os.path.join(project_dir, dir_name), exist_ok=True)
