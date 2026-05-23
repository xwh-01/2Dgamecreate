# FastAPI dependency injection setup
from functools import lru_cache

from .ai.image_generator import ImageGenerator
from .ai.prompt_builder import PromptBuilder
from .ai.quality_checker import QualityChecker
from .repositories.asset_repository import AssetRepository
from .repositories.export_repository import ExportRepository
from .repositories.generation_repository import GenerationRepository
from .repositories.project_repository import ProjectRepository
from .repositories.style_repository import StyleRepository
from .services.asset_service import AssetService
from .services.export_service import ExportService
from .services.generation_service import GenerationService
from .services.project_service import ProjectService
from .services.style_service import StyleService
from .storage.file_storage import FileStorage
from .storage.path_builder import PathBuilder
from .workflows.asset_generation_workflow import AssetGenerationWorkflow


@lru_cache
def get_path_builder() -> PathBuilder:
    return PathBuilder()


@lru_cache
def get_file_storage() -> FileStorage:
    return FileStorage(path_builder=get_path_builder())


@lru_cache
def get_project_repo() -> ProjectRepository:
    return ProjectRepository()


@lru_cache
def get_style_repo() -> StyleRepository:
    return StyleRepository()


@lru_cache
def get_generation_repo() -> GenerationRepository:
    return GenerationRepository()


@lru_cache
def get_asset_repo() -> AssetRepository:
    return AssetRepository()


@lru_cache
def get_export_repo() -> ExportRepository:
    return ExportRepository()


@lru_cache
def get_image_generator() -> ImageGenerator:
    return ImageGenerator()


@lru_cache
def get_prompt_builder() -> PromptBuilder:
    return PromptBuilder()


@lru_cache
def get_quality_checker() -> QualityChecker:
    return QualityChecker()


@lru_cache
def get_workflow() -> AssetGenerationWorkflow:
    return AssetGenerationWorkflow(
        generation_repo=get_generation_repo(),
        project_repo=get_project_repo(),
        style_repo=get_style_repo(),
        prompt_builder=get_prompt_builder(),
        image_generator=get_image_generator(),
        quality_checker=get_quality_checker(),
        file_storage=get_file_storage(),
        asset_repo=get_asset_repo(),
        path_builder=get_path_builder(),
    )


@lru_cache
def get_project_service() -> ProjectService:
    return ProjectService(project_repo=get_project_repo())


@lru_cache
def get_style_service() -> StyleService:
    return StyleService(style_repo=get_style_repo())


@lru_cache
def get_generation_service() -> GenerationService:
    return GenerationService(
        generation_repo=get_generation_repo(),
        workflow=get_workflow(),
    )


@lru_cache
def get_asset_service() -> AssetService:
    return AssetService(asset_repo=get_asset_repo(), file_storage=get_file_storage())


@lru_cache
def get_export_service() -> ExportService:
    return ExportService(export_repo=get_export_repo())
