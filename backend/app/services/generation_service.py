# Generation task orchestration service
import uuid
from typing import Optional

from ..domain.entities.generation_task import GenerationTask
from ..domain.enums.task_status import TaskStatus
from ..repositories.generation_repository import GenerationRepository
from ..schemas.generation_schema import GenerationCreateRequest
from ..utils.time import utcnow
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
        task = GenerationTask(
            id=str(uuid.uuid4()),
            project_id=request.project_id,
            asset_type=request.asset_type,
            status=TaskStatus.PENDING,
            user_input=request.description,
            size=request.size,
            parsed_requirement=request.extra_params.model_dump() if request.extra_params else {},
        )
        return self.repo.create(task)

    def get_task(self, task_id: str) -> Optional[GenerationTask]:
        return self.repo.get_by_id(task_id)

    def list_by_project(self, project_id: str) -> list[GenerationTask]:
        return self.repo.list_by_project_id(project_id)

    def cancel_task(self, task_id: str) -> Optional[GenerationTask]:
        return self.repo.mark_cancelled(task_id)

    def retry_task(self, task_id: str) -> Optional[GenerationTask]:
        task = self.repo.get_by_id(task_id)
        if task is None:
            return None
        task.status = TaskStatus.PENDING
        task.error_message = None
        self.repo.create(task)
        return task

    def run_task(self, task_id: str):
        return self.workflow.run(task_id)
