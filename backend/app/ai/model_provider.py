# Model provider registry and selection logic
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from .image_generator_client import ImageGeneratorClient


@dataclass
class ModelInfo:
    name: str
    provider: str
    supported_sizes: list[str]
    supports_transparency: bool = False


class ModelProvider(ABC):
    @abstractmethod
    def get_client(self, model_name: Optional[str] = None, **kwargs) -> ImageGeneratorClient:
        raise NotImplementedError

    @abstractmethod
    def list_models(self) -> list[ModelInfo]:
        raise NotImplementedError
