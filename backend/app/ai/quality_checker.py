# AI-powered quality assessment for generated images
from dataclasses import dataclass, field

from ..utils.image_utils import analyze_sprite_image, get_image_size, has_alpha, open_image
from .image_generator_client import GeneratedImage


@dataclass
class QualityCheckItem:
    name: str
    passed: bool
    message: str = ""


@dataclass
class QualityCheckResult:
    passed: bool
    checks: list = field(default_factory=list)
    overall_message: str = ""


class QualityChecker:
    def check(self, image: GeneratedImage, expected_size: str) -> QualityCheckResult:
        critical = []
        non_critical = []

        critical.append(self._check_image_exists(image))
        critical.append(self._check_is_png(image))
        critical.append(self._check_file_size(image))
        non_critical.append(self._check_size_match(image, expected_size))
        non_critical.append(self._check_alpha_channel(image))

        analysis = analyze_sprite_image(image.image_bytes)
        non_critical.append(self._check_transparent_background(analysis))
        non_critical.append(self._check_subject_fill_ratio(analysis))
        non_critical.append(self._check_centered_subject(analysis))
        non_critical.append(self._check_near_white_background_removed(analysis))

        all_critical_ok = all(c.passed for c in critical)
        all_checks = critical + non_critical
        messages = [c.message for c in all_checks if not c.passed]

        return QualityCheckResult(
            passed=all_critical_ok,
            checks=all_checks,
            overall_message="; ".join(messages) if messages else "All checks passed",
        )

    def _check_image_exists(self, image: GeneratedImage) -> QualityCheckItem:
        if image.image_bytes and len(image.image_bytes) > 0:
            return QualityCheckItem(name="image_exists", passed=True)
        return QualityCheckItem(name="image_exists", passed=False, message="Image bytes are empty")

    def _check_is_png(self, image: GeneratedImage) -> QualityCheckItem:
        img = open_image(image.image_bytes)
        if img is None:
            return QualityCheckItem(name="is_png", passed=False, message="Cannot open image with PIL")
        return QualityCheckItem(
            name="is_png",
            passed=img.format == "PNG" if img.format else False,
            message=f"Image format is {img.format}" if img.format else "Unknown format",
        )

    def _check_size_match(self, image: GeneratedImage, expected_size: str) -> QualityCheckItem:
        try:
            ew, eh = map(int, expected_size.lower().split("x"))
        except (ValueError, AttributeError):
            return QualityCheckItem(name="size_match", passed=True, message="No size constraint specified")

        aw, ah = get_image_size(image.image_bytes)
        if aw == 0 and ah == 0:
            return QualityCheckItem(name="size_match", passed=True, message="Could not determine image size")

        if abs(aw - ew) <= 2 and abs(ah - eh) <= 2:
            return QualityCheckItem(name="size_match", passed=True)
        return QualityCheckItem(
            name="size_match",
            passed=False,
            message=f"Expected {expected_size}, got {aw}x{ah}",
        )

    def _check_file_size(self, image: GeneratedImage) -> QualityCheckItem:
        size = len(image.image_bytes)
        if size == 0:
            return QualityCheckItem(name="file_size", passed=False, message="File size is 0 bytes")
        if size > 50 * 1024 * 1024:
            return QualityCheckItem(name="file_size", passed=False, message=f"File too large: {size} bytes")
        return QualityCheckItem(name="file_size", passed=True)

    def _check_alpha_channel(self, image: GeneratedImage) -> QualityCheckItem:
        if has_alpha(image.image_bytes):
            return QualityCheckItem(name="alpha_channel", passed=True)
        return QualityCheckItem(
            name="alpha_channel",
            passed=False,
            message="Image does not have alpha channel for transparent background",
        )

    def _check_transparent_background(self, analysis: dict) -> QualityCheckItem:
        if analysis.get("error"):
            return QualityCheckItem(
                name="transparent_background",
                passed=True,
                message="Could not analyze image",
            )
        if not analysis.get("has_alpha", False):
            return QualityCheckItem(
                name="transparent_background",
                passed=False,
                message="Image has no alpha channel for transparency",
            )
        return QualityCheckItem(name="transparent_background", passed=True)

    def _check_subject_fill_ratio(self, analysis: dict) -> QualityCheckItem:
        if analysis.get("error"):
            return QualityCheckItem(
                name="subject_fill_ratio",
                passed=True,
                message="Could not analyze image",
            )
        ratio = analysis.get("subject_fill_ratio", 0.0)
        if ratio <= 0:
            return QualityCheckItem(
                name="subject_fill_ratio",
                passed=False,
                message="No visible subject found (alpha bbox empty)",
            )
        if ratio < 0.55:
            return QualityCheckItem(
                name="subject_fill_ratio",
                passed=False,
                message=f"Subject fill ratio {ratio:.2f} is below 0.55 — subject may be too small",
            )
        return QualityCheckItem(name="subject_fill_ratio", passed=True)

    def _check_centered_subject(self, analysis: dict) -> QualityCheckItem:
        if analysis.get("error"):
            return QualityCheckItem(
                name="centered_subject",
                passed=True,
                message="Could not analyze image",
            )
        offset = analysis.get("center_offset_ratio", 1.0)
        if offset > 0.18:
            return QualityCheckItem(
                name="centered_subject",
                passed=False,
                message=f"Center offset ratio {offset:.2f} is above 0.18 — subject may be off-center",
            )
        return QualityCheckItem(name="centered_subject", passed=True)

    def _check_near_white_background_removed(self, analysis: dict) -> QualityCheckItem:
        if analysis.get("error"):
            return QualityCheckItem(
                name="near_white_background",
                passed=True,
                message="Could not analyze image",
            )
        ratio = analysis.get("near_white_background_ratio", 0.0)
        if ratio > 0.25:
            return QualityCheckItem(
                name="near_white_background",
                passed=False,
                message=f"Near-white background ratio {ratio:.2f} is above 0.25 — image may still have white background remnants",
            )
        return QualityCheckItem(name="near_white_background", passed=True)
