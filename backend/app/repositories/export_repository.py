# Export package data access layer
from typing import Optional

from ..db.session import get_session
from ..domain.entities.export_package import ExportPackage
from ..utils.time import utcnow


class ExportRepository:
    def get_by_id(self, export_id: str) -> Optional[ExportPackage]:
        data = get_session().exports.get(export_id)
        if data is None:
            return None
        return ExportPackage(**data)

    def list_by_project_id(self, project_id: str) -> list[ExportPackage]:
        items = get_session().exports.list_by("project_id", project_id)
        return [ExportPackage(**item) for item in items]

    def create(self, export_package: ExportPackage) -> ExportPackage:
        export_package.created_at = utcnow()
        export_package.updated_at = utcnow()
        get_session().exports.set(export_package.id, {
            "id": export_package.id,
            "project_id": export_package.project_id,
            "status": export_package.status.value,
            "file_path": export_package.file_path,
            "engine_type": export_package.engine_type,
            "created_at": export_package.created_at.isoformat(),
            "updated_at": export_package.updated_at.isoformat(),
        })
        return export_package

    def update(self, export_id: str, data_dict: dict) -> Optional[ExportPackage]:
        existing = get_session().exports.get(export_id)
        if existing is None:
            return None
        existing.update(data_dict)
        existing["updated_at"] = utcnow().isoformat()
        get_session().exports.set(export_id, existing)
        return ExportPackage(**existing)

    def delete(self, export_id: str) -> bool:
        return get_session().exports.delete(export_id)
