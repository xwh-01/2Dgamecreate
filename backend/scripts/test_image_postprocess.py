"""Minimal test for sprite post-processing pipeline.

Creates a 512x512 white-background image with a red 100x100 square off-center,
runs normalize_sprite_canvas, saves the result, and prints analysis.
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.image_utils import (
    analyze_sprite_image,
    encode_png,
    image_bytes_to_rgba,
    normalize_sprite_canvas,
)


def main():
    w, h = 512, 512
    img = Image.new("RGBA", (w, h), (255, 255, 255, 255))

    square_size = 100
    square_x = 60
    square_y = 80
    for x in range(square_x, square_x + square_size):
        for y in range(square_y, square_y + square_size):
            img.putpixel((x, y), (255, 0, 0, 255))

    raw_bytes = encode_png(img)

    print("=== Before normalize_sprite_canvas ===")
    pre_analysis = analyze_sprite_image(raw_bytes)
    for key, value in pre_analysis.items():
        print(f"  {key}: {value}")

    result_bytes = normalize_sprite_canvas(raw_bytes, "512x512")

    os.makedirs("tmp", exist_ok=True)
    result_img = image_bytes_to_rgba(result_bytes)
    result_img.save("tmp/postprocess_result.png")

    print()
    print("=== After normalize_sprite_canvas ===")
    post_analysis = analyze_sprite_image(result_bytes)
    for key, value in post_analysis.items():
        print(f"  {key}: {value}")

    assert result_img.mode == "RGBA", "Output must have alpha channel"
    assert result_img.size == (512, 512), f"Output size must be 512x512, got {result_img.size}"

    bbox = post_analysis["alpha_bbox"]
    assert bbox is not None, "Alpha bbox must not be empty"
    assert bbox[2] > bbox[0] and bbox[3] > bbox[1], "Bbox must have positive area"

    assert post_analysis["near_white_background_ratio"] < 0.1, (
        "Near-white background should be removed"
    )

    assert post_analysis["subject_fill_ratio"] > 0.01, (
        "Subject should occupy some canvas area"
    )

    assert post_analysis["center_offset_ratio"] < 0.15, (
        f"Subject should be near center, got offset {post_analysis['center_offset_ratio']}"
    )

    print()
    print("All assertions passed.")
    print(f"Result saved to tmp/postprocess_result.png")


if __name__ == "__main__":
    main()
