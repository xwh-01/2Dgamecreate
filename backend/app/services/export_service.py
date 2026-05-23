# Export and packaging service
from typing import Optional

from ..domain.entities.export_package import ExportPackage
from ..repositories.export_repository import ExportRepository


class ExportService:
    def __init__(self, export_repo: ExportRepository):
        self.repo = export_repo

    def create_export(self, project_id: str, engine_type: Optional[str] = None) -> ExportPackage:
        raise NotImplementedError

    def get_export(self, export_id: str) -> Optional[ExportPackage]:
        raise NotImplementedError

    def list_by_project(self, project_id: str) -> list[ExportPackage]:
        raise NotImplementedError
