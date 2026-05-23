# AI-powered quality assessment for generated images
from dataclasses import dataclass, field

from .image_generator import GeneratedImage


@dataclass
class QualityCheckItem:
    name: str
    passed: bool
    message: str = ""


@dataclass
class QualityCheckResult:
    passed: bool
    checks: list[QualityCheckItem] = field(default_factory=list)
    overall_message: str = ""


class QualityChecker:
    def check(self, image: GeneratedImage, expected_size: str) -> QualityCheckResult:
        raise NotImplementedError

    def _check_image_exists(self, image: GeneratedImage) -> QualityCheckItem:
        raise NotImplementedError

    def _check_is_png(self, image: GeneratedImage) -> QualityCheckItem:
        raise NotImplementedError

    def _check_size_match(self, image: GeneratedImage, expected_size: str) -> QualityCheckItem:
        raise NotImplementedError

    def _check_alpha_channel(self, image: GeneratedImage) -> QualityCheckItem:
        raise NotImplementedError

    def _check_file_size(self, image: GeneratedImage) -> QualityCheckItem:
        raise NotImplementedError
