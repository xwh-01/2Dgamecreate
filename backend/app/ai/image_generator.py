# Image generation coordinator (selects model, manages retries)
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .prompt_builder import PromptPackage


@dataclass
class GeneratedImage:
    image_bytes: bytes
    width: int
    height: int
    format: str = "png"


class ImageGenerator(ABC):
    @abstractmethod
    def generate(self, prompt_package: PromptPackage, size: str) -> GeneratedImage:
        raise NotImplementedError
