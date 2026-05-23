# Model provider registry and selection logic
from dataclasses import dataclass

from ..config import get_settings
from .image_generator_client import ImageGeneratorClient, OpenAIImageClient


@dataclass
class ModelInfo:
    name: str
    provider: str
    supported_sizes: list
    supports_transparency: bool = False


class ModelProvider:
    def get_client(self, model_name: str = "", **kwargs) -> ImageGeneratorClient:
        settings = get_settings()
        provider = model_name or settings.image_provider

        if provider == "openai":
            return OpenAIImageClient(
                api_key=settings.image_api_key,
                model=settings.image_model,
            )
        raise RuntimeError(f"Unsupported image provider: {provider}")

    def list_models(self) -> list[ModelInfo]:
        return [
            ModelInfo(
                name="dall-e-3",
                provider="openai",
                supported_sizes=["1024x1024", "1024x1792", "1792x1024"],
            ),
        ]
