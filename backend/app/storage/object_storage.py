# Object storage operations (S3-compatible)
from abc import ABC, abstractmethod


class ObjectStorage(ABC):
    @abstractmethod
    def save(self, key: str, data: bytes, content_type: str = "image/png") -> str:
        raise NotImplementedError

    @abstractmethod
    def read(self, key: str) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_url(self, key: str) -> str:
        raise NotImplementedError
