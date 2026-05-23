# Asset generation workflow orchestrator
import logging
from dataclasses import dataclass, field
from typing import Any, Optional

from ..ai.image_generator import GeneratedImage, ImageGenerator
from ..ai.prompt_builder import PromptBuilder, PromptPackage
from ..ai.quality_checker import QualityCheckResult
from ..domain.entities.asset import Asset
from ..domain.entities.generation_task import GenerationTask
from ..domain.entities.project import Project
from ..domain.entities.style_profile import StyleProfile
from ..domain.enums.task_status import TaskStatus
from ..repositories.asset_repository import AssetRepository
from ..repositories.generation_repository import GenerationRepository
from ..repositories.project_repository import ProjectRepository
from ..repositories.style_repository import StyleRepository
from ..storage.file_storage import FileStorage
from ..storage.path_builder import PathBuilder
from .steps.build_prompt_step import BuildPromptStep
from .steps.generate_image_step import GenerateImageStep
from .steps.parse_requirement_step import ParseRequirementStep
from .steps.post_process_step import PostProcessStep
from .steps.quality_check_step import QualityCheckStep
from .steps.save_asset_step import SaveAssetStep

logger = logging.getLogger(__name__)


@dataclass
class WorkflowContext:
    task_id: str
    task: Optional[GenerationTask] = None
    project: Optional[Project] = None
    style_profile: Optional[StyleProfile] = None
    parsed_requirement: Optional[Any] = None
    prompt_package: Optional[PromptPackage] = None
    generated_image: Optional[GeneratedImage] = None
    processed_image: Optional[GeneratedImage] = None
    quality_result: Optional[QualityCheckResult] = None
    saved_path: Optional[str] = None
    asset_record: Optional[Asset] = None
    error_message: Optional[str] = None


class AssetGenerationWorkflow:
    def __init__(
        self,
        generation_repo: GenerationRepository,
        project_repo: ProjectRepository,
        style_repo: StyleRepository,
        requirement_parser: Any,
        prompt_builder: PromptBuilder,
        image_generator: ImageGenerator,
        quality_checker: Any,
        file_storage: FileStorage,
        asset_repo: AssetRepository,
        path_builder: PathBuilder,
    ):
        self.generation_repo = generation_repo
        self.project_repo = project_repo
        self.style_repo = style_repo
        self.requirement_parser = requirement_parser
        self.prompt_builder = prompt_builder
        self.image_generator = image_generator
        self.quality_checker = quality_checker
        self.file_storage = file_storage
        self.asset_repo = asset_repo
        self.path_builder = path_builder

        self.steps = [
            ParseRequirementStep(),
            BuildPromptStep(),
            GenerateImageStep(),
            PostProcessStep(),
            QualityCheckStep(),
            SaveAssetStep(),
        ]

    def run(self, task_id: str) -> WorkflowContext:
        ctx = WorkflowContext(task_id=task_id)

        try:
            ctx = self._load_task(ctx)
            ctx = self._mark_running(ctx)
            ctx = self._load_project_and_style(ctx)

            for step in self.steps:
                ctx = step.execute(ctx, self)
                if ctx.error_message:
                    raise RuntimeError(ctx.error_message)

            ctx = self._mark_succeeded(ctx)
            return ctx

        except Exception as exc:
            logger.error(f"Workflow failed for task {task_id}: {exc}")
            ctx.error_message = str(exc)
            ctx = self._mark_failed(ctx)
            return ctx

    def _load_task(self, ctx: WorkflowContext) -> WorkflowContext:
        ctx.task = self.generation_repo.get_by_id(ctx.task_id)
        if ctx.task is None:
            ctx.error_message = f"Task not found: {ctx.task_id}"
        return ctx

    def _mark_running(self, ctx: WorkflowContext) -> WorkflowContext:
        self.generation_repo.mark_running(ctx.task_id)
        ctx.task.status = TaskStatus.RUNNING
        return ctx

    def _load_project_and_style(self, ctx: WorkflowContext) -> WorkflowContext:
        if ctx.task is None:
            return ctx
        ctx.project = self.project_repo.get_by_id(ctx.task.project_id)
        if ctx.project and ctx.project.style_profile_id:
            ctx.style_profile = self.style_repo.get_by_id(ctx.project.style_profile_id)
        return ctx

    def _mark_succeeded(self, ctx: WorkflowContext) -> WorkflowContext:
        if ctx.asset_record:
            self.generation_repo.mark_succeeded(ctx.task_id, ctx.asset_record.id)
            ctx.task.status = TaskStatus.SUCCEEDED
        return ctx

    def _mark_failed(self, ctx: WorkflowContext) -> WorkflowContext:
        self.generation_repo.mark_failed(
            ctx.task_id, ctx.error_message or "Unknown error"
        )
        if ctx.task:
            ctx.task.status = TaskStatus.FAILED
        return ctx
