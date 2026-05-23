# Export and packaging service
import uuid
from typing import Optional

from ..domain.entities.export_package import ExportPackage, ExportStatus
from ..repositories.export_repository import ExportRepository


class ExportService:
    def __init__(self, export_repo: ExportRepository):
        self.repo = export_repo

    def create_export(self, project_id: str, engine_type: Optional[str] = None) -> ExportPackage:
        pkg = ExportPackage(
            id=str(uuid.uuid4()),
            project_id=project_id,
            status=ExportStatus.PENDING,
            engine_type=engine_type,
        )
        return self.repo.create(pkg)

    def get_export(self, export_id: str) -> Optional[ExportPackage]:
        return self.repo.get_by_id(export_id)

    def list_by_project(self, project_id: str) -> list[ExportPackage]:
        return self.repo.list_by_project_id(project_id)
