# Workflow context - shared data class used between workflow and steps
from dataclasses import dataclass, field
from typing import Any, Optional

from ..ai.image_generator_client import GeneratedImage
from ..ai.prompt_builder import PromptPackage
from ..ai.quality_checker import QualityCheckResult
from ..domain.entities.asset import Asset
from ..domain.entities.generation_task import GenerationTask
from ..domain.entities.project import Project
from ..domain.entities.style_profile import StyleProfile


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
