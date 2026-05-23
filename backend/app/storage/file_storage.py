# Local file system storage operations
from abc import ABC, abstractmethod


class FileStorage(ABC):
    @abstractmethod
    def save(self, file_path: str, data: bytes) -> str:
        raise NotImplementedError

    @abstractmethod
    def read(self, file_path: str) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def delete(self, file_path: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_url(self, file_path: str) -> str:
        raise NotImplementedError
