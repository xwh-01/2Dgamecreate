# Image generation coordinator (selects model, manages retries)
from ..config import get_settings
from .image_generator_client import (
    GeneratedImage,
    OpenAIImageClient,
    TongyiWanxiangClient,
)
from .prompt_builder import PromptPackage


class ImageGenerator:
    def __init__(self):
        settings = get_settings()
        self.provider = settings.image_provider
        self.api_key = settings.image_api_key
        self.model = settings.image_model

    def generate(self, prompt_package: PromptPackage, size: str) -> GeneratedImage:
        if not self.api_key:
            raise RuntimeError("image provider is not configured")

        full_prompt = prompt_package.to_full_prompt()
        negative = prompt_package.to_full_negative_prompt()

        if self.provider == "openai":
            client = OpenAIImageClient(api_key=self.api_key, model=self.model)
        elif self.provider == "tongyi":
            client = TongyiWanxiangClient(api_key=self.api_key, model=self.model)
        else:
            raise RuntimeError(f"Unsupported image provider: {self.provider}")

        return client.generate(
            prompt=full_prompt,
            negative_prompt=negative,
            size=size,
        )
