# Export package data access layer
from typing import Optional

from ..domain.entities.export_package import ExportPackage


class ExportRepository:
    def get_by_id(self, export_id: str) -> Optional[ExportPackage]:
        raise NotImplementedError

    def list_by_project_id(self, project_id: str) -> list[ExportPackage]:
        raise NotImplementedError

    def create(self, export_package: ExportPackage) -> ExportPackage:
        raise NotImplementedError

    def update(self, export_id: str, data: dict) -> Optional[ExportPackage]:
        raise NotImplementedError

    def delete(self, export_id: str) -> bool:
        raise NotImplementedError
