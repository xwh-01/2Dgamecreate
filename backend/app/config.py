# Application configuration and settings
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    image_provider: str = ""
    image_api_key: str = ""
    image_model: str = "dall-e-3"

    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-chat"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
