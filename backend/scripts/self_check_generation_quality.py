"""Self-checks for prompt quality, sprite normalization, and quality checker behavior."""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ai.image_generator_client import GeneratedImage
from app.ai.prompt_builder import PromptBuilder
from app.ai.quality_checker import QualityChecker
from app.ai.requirement_parser import ParsedRequirement
from app.domain.enums.asset_type import AssetType
from app.utils.image_utils import encode_png, normalize_sprite_canvas, open_image


def build_enemy_requirement() -> ParsedRequirement:
    return ParsedRequirement(
        asset_type=AssetType.ENEMY,
        subject="red horned demon",
        size="64x64",
        background="transparent",
        name="red demon",
        view="front",
        action="attacking",
        pose="attacking",
        camera_angle="front",
        body_ratio="chibi",
        canvas_fill="85%",
        outline_style="pixel",
        color_palette="red, black, gold",
        emotion="angry",
        complexity="simple",
        animation_frame="attack_1",
        appearance="small red demon with black horns and sharp teeth",
        weapon="claws",
        forbidden_elements=["text", "watermark", "white background"],
    )


def make_test_image() -> bytes:
    img = Image.new("RGBA", (64, 64), (40, 48, 58, 255))
    for x in range(22, 42):
        for y in range(12, 52):
            img.putpixel((x, y), (220, 30, 40, 255))
    return encode_png(img)


def main():
    parsed = build_enemy_requirement()
    prompt = PromptBuilder().build(parsed)
    full_prompt = prompt.to_full_prompt()

    required_prompt_terms = [
        "Subject:",
        "Composition:",
        "Style:",
        "Technical:",
        "Negative constraints:",
        "enemy sprite",
        "attacking pose",
        "angry expression",
        "red, black, gold color palette",
        "pixel outline",
        "85%",
    ]
    for term in required_prompt_terms:
        assert term in full_prompt, f"Prompt missing expected term: {term}"

    normalized = normalize_sprite_canvas(make_test_image(), "64x64")
    normalized_img = open_image(normalized)
    assert normalized_img is not None, "Normalized image must be readable"
    assert normalized_img.format == "PNG", "Normalized output must be PNG"
    assert normalized_img.size == (64, 64), f"Expected 64x64, got {normalized_img.size}"

    checker = QualityChecker()
    tiny = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    tiny.putpixel((32, 32), (255, 0, 0, 255))
    result = checker.check(
        GeneratedImage(image_bytes=encode_png(tiny), width=64, height=64),
        "64x64",
        parsed_requirement=parsed,
        prompt_package=prompt,
    )
    assert result.passed is True, "Non-critical quality warnings must not fail workflow"
    assert isinstance(result.issues, list), "Quality result should expose issues"
    assert result.semantic_check_result is not None, "Semantic check extension result missing"
    assert result.style_check_result is not None, "Style check extension result missing"

    print("Generation quality self-check passed.")


if __name__ == "__main__":
    main()
