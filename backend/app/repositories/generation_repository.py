# Generation task data access layer
from typing import Optional

from ..domain.entities.generation_task import GenerationTask


class GenerationRepository:
    def get_by_id(self, task_id: str) -> Optional[GenerationTask]:
        raise NotImplementedError

    def create(self, task: GenerationTask) -> GenerationTask:
        raise NotImplementedError

    def mark_running(self, task_id: str) -> Optional[GenerationTask]:
        raise NotImplementedError

    def mark_succeeded(self, task_id: str, result_asset_id: str) -> Optional[GenerationTask]:
        raise NotImplementedError

    def mark_failed(self, task_id: str, error_message: str) -> Optional[GenerationTask]:
        raise NotImplementedError

    def mark_cancelled(self, task_id: str) -> Optional[GenerationTask]:
        raise NotImplementedError

    def list_by_project_id(self, project_id: str) -> list[GenerationTask]:
        raise NotImplementedError
