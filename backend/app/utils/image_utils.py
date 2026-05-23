# Image processing utilities (crop, resize, format conversion)
import io
from typing import Optional

from PIL import Image


def open_image(data: bytes) -> Optional[Image.Image]:
    try:
        return Image.open(io.BytesIO(data))
    except Exception:
        return None


def ensure_png(image: Image.Image) -> bytes:
    buf = io.BytesIO()
    if image.mode in ("RGBA", "LA", "P"):
        image = image.convert("RGBA")
    else:
        image = image.convert("RGB")
    image.save(buf, format="PNG")
    return buf.getvalue()


def resize_to_target(image: Image.Image, target_size: str) -> Image.Image:
    try:
        w, h = map(int, target_size.lower().split("x"))
        return image.resize((w, h), Image.LANCZOS)
    except (ValueError, AttributeError):
        return image


def get_image_size(data: bytes) -> tuple[int, int]:
    img = open_image(data)
    if img is None:
        return (0, 0)
    return img.size


def has_alpha(data: bytes) -> bool:
    img = open_image(data)
    if img is None:
        return False
    return img.mode in ("RGBA", "LA") or "transparency" in img.info
