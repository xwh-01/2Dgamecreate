# AI-assisted and heuristic quality assessment for generated images
from dataclasses import dataclass, field
from typing import Any, Optional

from ..config import get_settings
from ..utils.image_utils import analyze_sprite_image, get_image_size, has_alpha, open_image
from .image_generator_client import GeneratedImage


@dataclass
class QualityCheckItem:
    name: str
    passed: bool
    message: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "passed": self.passed,
            "message": self.message,
        }


@dataclass
class QualityCheckResult:
    passed: bool
    checks: list[QualityCheckItem] = field(default_factory=list)
    overall_message: str = ""
    subject_match: Optional[bool] = None
    style_match: Optional[bool] = None
    background_ok: Optional[bool] = None
    full_body_ok: Optional[bool] = None
    no_text_ok: Optional[bool] = None
    issues: list[str] = field(default_factory=list)
    semantic_check_result: Optional[dict] = None
    style_check_result: Optional[dict] = None

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "checks": [c.to_dict() for c in self.checks],
            "overall_message": self.overall_message,
            "subject_match": self.subject_match,
            "style_match": self.style_match,
            "background_ok": self.background_ok,
            "full_body_ok": self.full_body_ok,
            "no_text_ok": self.no_text_ok,
            "issues": self.issues,
            "semantic_check_result": self._serialize_extension(self.semantic_check_result),
            "style_check_result": self._serialize_extension(self.style_check_result),
        }

    def _serialize_extension(self, result: Optional[dict]) -> Optional[dict]:
        if result is None:
            return None
        serialized = dict(result)
        serialized["checks"] = [
            c.to_dict() if hasattr(c, "to_dict") else c
            for c in serialized.get("checks", [])
        ]
        return serialized


class QualityChecker:
    def check(
        self,
        image: GeneratedImage,
        expected_size: str,
        parsed_requirement: Optional[Any] = None,
        prompt_package: Optional[Any] = None,
        style_profile: Optional[dict] = None,
    ) -> QualityCheckResult:
        critical = [
            self._check_image_exists(image),
            self._check_is_png(image),
            self._check_file_size(image),
        ]
        non_critical = [
            self._check_size_match(image, expected_size),
            self._check_alpha_channel(image),
        ]

        analysis = analyze_sprite_image(image.image_bytes)
        non_critical.extend(
            [
                self._check_transparent_background(analysis),
                self._check_subject_fill_ratio(analysis),
                self._check_centered_subject(analysis),
                self._check_near_white_background_removed(analysis),
            ]
        )

        semantic_result = self.semantic_check_result(
            image=image,
            parsed_requirement=parsed_requirement,
            prompt_package=prompt_package,
        )
        style_result = self.style_check_result(
            image=image,
            parsed_requirement=parsed_requirement,
            prompt_package=prompt_package,
            style_profile=style_profile,
        )

        non_critical.extend(semantic_result.get("checks", []))
        non_critical.extend(style_result.get("checks", []))

        all_critical_ok = all(c.passed for c in critical)
        all_checks = critical + non_critical
        issues = [c.message for c in all_checks if not c.passed and c.message]
        background_ok = self._check_by_name(all_checks, "transparent_background")
        full_body_ok = self._infer_full_body_ok(parsed_requirement, all_checks)
        no_text_ok = self._check_by_name(all_checks, "no_text")

        return QualityCheckResult(
            passed=all_critical_ok,
            checks=all_checks,
            overall_message="; ".join(issues) if issues else "All critical checks passed",
            subject_match=semantic_result.get("subject_match"),
            style_match=style_result.get("style_match"),
            background_ok=background_ok,
            full_body_ok=full_body_ok,
            no_text_ok=no_text_ok,
            issues=issues,
            semantic_check_result=semantic_result,
            style_check_result=style_result,
        )

    def semantic_check_result(
        self,
        image: GeneratedImage,
        parsed_requirement: Optional[Any] = None,
        prompt_package: Optional[Any] = None,
    ) -> dict:
        settings = get_settings()
        if not settings.vision_model_api_key:
            return {
                "skipped": True,
                "reason": "VISION_MODEL_API_KEY is not configured",
                "subject_match": None,
                "checks": [
                    QualityCheckItem(
                        name="subject_match",
                        passed=True,
                        message="Semantic subject check skipped",
                    ),
                    QualityCheckItem(
                        name="no_text",
                        passed=True,
                        message="Text detection skipped",
                    ),
                ],
            }

        # Extension point for a future visual model call. Keep non-blocking.
        return {
            "skipped": True,
            "reason": "Vision model semantic check is not implemented yet",
            "subject_match": None,
            "checks": [
                QualityCheckItem(
                    name="subject_match",
                    passed=True,
                    message="Semantic subject check not implemented",
                ),
                QualityCheckItem(
                    name="no_text",
                    passed=True,
                    message="Text detection not implemented",
                ),
            ],
        }

    def style_check_result(
        self,
        image: GeneratedImage,
        parsed_requirement: Optional[Any] = None,
        prompt_package: Optional[Any] = None,
        style_profile: Optional[dict] = None,
    ) -> dict:
        settings = get_settings()
        if not settings.vision_model_api_key:
            return {
                "skipped": True,
                "reason": "VISION_MODEL_API_KEY is not configured",
                "style_match": None,
                "checks": [
                    QualityCheckItem(
                        name="style_match",
                        passed=True,
                        message="Style check skipped",
                    )
                ],
            }

        # Extension point for a future visual model call. Keep non-blocking.
        return {
            "skipped": True,
            "reason": "Vision model style check is not implemented yet",
            "style_match": None,
            "checks": [
                QualityCheckItem(
                    name="style_match",
                    passed=True,
                    message="Style check not implemented",
                )
            ],
        }

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
                message=f"Subject fill ratio {ratio:.2f} is below 0.55; subject may be too small",
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
                message=f"Center offset ratio {offset:.2f} is above 0.18; subject may be off-center",
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
                message=f"Near-white background ratio {ratio:.2f} is above 0.25; white remnants may remain",
            )
        return QualityCheckItem(name="near_white_background", passed=True)

    def _check_by_name(self, checks: list[QualityCheckItem], name: str) -> Optional[bool]:
        for check in checks:
            if check.name == name:
                return check.passed
        return None

    def _infer_full_body_ok(
        self,
        parsed_requirement: Optional[Any],
        checks: list[QualityCheckItem],
    ) -> Optional[bool]:
        asset_type = getattr(parsed_requirement, "asset_type", None)
        asset_value = getattr(asset_type, "value", asset_type)
        if asset_value not in ("character", "enemy"):
            return None
        return self._check_by_name(checks, "subject_fill_ratio")
