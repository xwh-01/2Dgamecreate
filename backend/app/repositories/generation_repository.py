# Generation task data access layer
from typing import Optional

from ..db.session import get_session
from ..domain.entities.generation_task import GenerationTask
from ..domain.enums.task_status import TaskStatus
from ..utils.time import utcnow


class GenerationRepository:
    def get_by_id(self, task_id: str) -> Optional[GenerationTask]:
        data = get_session().tasks.get(task_id)
        if data is None:
            return None
        return GenerationTask(**data)

    def create(self, task: GenerationTask) -> GenerationTask:
        task.created_at = utcnow()
        task.updated_at = utcnow()
        get_session().tasks.set(task.id, {
            "id": task.id,
            "project_id": task.project_id,
            "asset_type": task.asset_type.value,
            "status": task.status.value,
            "user_input": task.user_input,
            "parsed_requirement": task.parsed_requirement,
            "final_prompt": task.final_prompt,
            "model_name": task.model_name,
            "size": task.size,
            "error_message": task.error_message,
            "result_asset_id": task.result_asset_id,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
        })
        return task

    def _update_status(self, task_id: str, update: dict) -> Optional[GenerationTask]:
        existing = get_session().tasks.get(task_id)
        if existing is None:
            return None
        existing.update(update)
        existing["updated_at"] = utcnow().isoformat()
        get_session().tasks.set(task_id, existing)
        return GenerationTask(**existing)

    def mark_running(self, task_id: str) -> Optional[GenerationTask]:
        return self._update_status(task_id, {"status": "running"})

    def mark_succeeded(self, task_id: str, result_asset_id: str) -> Optional[GenerationTask]:
        return self._update_status(task_id, {"status": "succeeded", "result_asset_id": result_asset_id})

    def mark_failed(self, task_id: str, error_message: str) -> Optional[GenerationTask]:
        return self._update_status(task_id, {"status": "failed", "error_message": error_message})

    def mark_cancelled(self, task_id: str) -> Optional[GenerationTask]:
        return self._update_status(task_id, {"status": "cancelled"})

    def list_by_project_id(self, project_id: str) -> list[GenerationTask]:
        items = get_session().tasks.list_by("project_id", project_id)
        return [GenerationTask(**item) for item in items]
