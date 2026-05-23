# Abstract interface for image generation model clients
from abc import ABC, abstractmethod
from dataclasses import dataclass

from openai import OpenAI


@dataclass
class GeneratedImage:
    image_bytes: bytes
    width: int
    height: int
    format: str = "png"


class ImageGeneratorClient(ABC):
    @abstractmethod
    def generate(self, prompt: str, negative_prompt: str, size: str, **kwargs) -> GeneratedImage:
        raise NotImplementedError


class OpenAIImageClient(ImageGeneratorClient):
    def __init__(self, api_key: str, model: str = "dall-e-3"):
        self.api_key = api_key
        self.model = model
        self._client = OpenAI(api_key=api_key)

    def generate(self, prompt: str, negative_prompt: str, size: str, **kwargs) -> GeneratedImage:
        import requests

        if not self.api_key:
            raise RuntimeError("image provider is not configured")

        full_prompt = prompt
        if negative_prompt:
            full_prompt = f"{prompt}. IMPORTANT: avoid {negative_prompt}"

        try:
            response = self._client.images.generate(
                model=self.model,
                prompt=full_prompt,
                n=1,
                size=self._map_size(size),
                quality="standard",
                response_format="url",
            )

            image_url = response.data[0].url
            if image_url is None:
                raise RuntimeError("No image URL in response")

            img_response = requests.get(image_url, timeout=60)
            img_response.raise_for_status()
            image_bytes = img_response.content

            return GeneratedImage(
                image_bytes=image_bytes,
                width=0,
                height=0,
                format="png",
            )
        except Exception as e:
            raise RuntimeError(f"Image generation failed: {str(e)}") from e

    def _map_size(self, size: str) -> str:
        size_map = {
            "32x32": "1024x1024",
            "64x64": "1024x1024",
            "128x128": "1024x1024",
            "256x256": "1024x1024",
        }
        return size_map.get(size, "1024x1024")


class TongyiWanxiangClient(ImageGeneratorClient):
    def __init__(self, api_key: str, model: str = "wanx2.1-t2i-turbo"):
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str, negative_prompt: str, size: str, **kwargs) -> GeneratedImage:
        import requests
        from dashscope import ImageSynthesis

        if not self.api_key:
            raise RuntimeError("image provider is not configured")

        full_prompt = prompt
        if negative_prompt:
            full_prompt = f"{prompt}. Avoid: {negative_prompt}"

        wanx_size = self._map_size(size)

        try:
            response = ImageSynthesis.call(
                model=self.model,
                prompt=prompt,
                n=1,
                size=wanx_size,
                api_key=self.api_key,
            )

            if response.status_code != 200:
                raise RuntimeError(f"Tongyi Wanxiang error: {response.code} {response.message}")

            image_url = response.output.results[0].url
            if not image_url:
                raise RuntimeError("No image URL in response")

            img_response = requests.get(image_url, timeout=60)
            img_response.raise_for_status()

            return GeneratedImage(
                image_bytes=img_response.content,
                width=0,
                height=0,
                format="png",
            )
        except Exception as e:
            raise RuntimeError(f"Tongyi Wanxiang generation failed: {str(e)}") from e

    def _map_size(self, size: str) -> str:
        size_map = {
            "32x32": "1024*1024",
            "64x64": "1024*1024",
            "128x128": "1024*1024",
            "256x256": "1024*1024",
        }
        return size_map.get(size, "1024*1024")
