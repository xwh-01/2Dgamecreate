# Abstract interface for image generation model clients
from abc import ABC, abstractmethod

from .image_generator import GeneratedImage


class ImageGeneratorClient(ABC):
    @abstractmethod
    def generate(self, prompt: str, negative_prompt: str, size: str, **kwargs) -> GeneratedImage:
        raise NotImplementedError
