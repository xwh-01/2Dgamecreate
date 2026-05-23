# Generation task orchestration service
from typing import Optional

from ..domain.entities.generation_task import GenerationTask
from ..repositories.generation_repository import GenerationRepository
from ..schemas.generation_schema import GenerationCreateRequest
from ..workflows.asset_generation_workflow import AssetGenerationWorkflow


class GenerationService:
    def __init__(
        self,
        generation_repo: GenerationRepository,
        workflow: AssetGenerationWorkflow,
    ):
        self.repo = generation_repo
        self.workflow = workflow

    def create_task(self, request: GenerationCreateRequest) -> GenerationTask:
        raise NotImplementedError

    def get_task(self, task_id: str) -> Optional[GenerationTask]:
        raise NotImplementedError

    def list_by_project(self, project_id: str) -> list[GenerationTask]:
        raise NotImplementedError

    def cancel_task(self, task_id: str) -> Optional[GenerationTask]:
        raise NotImplementedError

    def retry_task(self, task_id: str) -> Optional[GenerationTask]:
        raise NotImplementedError

    def run_task(self, task_id: str):
        raise NotImplementedError
