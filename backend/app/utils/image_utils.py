# Image processing utilities (crop, resize, format conversion, sprite normalization)
import io
from collections import Counter, deque
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


def image_bytes_to_rgba(image_bytes: bytes) -> Optional[Image.Image]:
    img = open_image(image_bytes)
    if img is None:
        return None
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    return img


def encode_png(image: Image.Image) -> bytes:
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()


def get_alpha_bbox(image: Image.Image):
    if image.mode != "RGBA":
        return None
    alpha = image.split()[-1]
    return alpha.getbbox()


def remove_near_white_background(image_bytes: bytes, threshold: int = 245) -> bytes:
    img = image_bytes_to_rgba(image_bytes)
    if img is None:
        return image_bytes
    pixels = list(img.getdata())
    new_pixels = []
    for r, g, b, a in pixels:
        if r >= threshold and g >= threshold and b >= threshold:
            new_pixels.append((r, g, b, 0))
        else:
            new_pixels.append((r, g, b, a))
    img.putdata(new_pixels)
    return encode_png(img)


def remove_uniform_edge_background(
    image_bytes: bytes,
    color_tolerance: int = 24,
    min_edge_ratio: float = 0.35,
) -> bytes:
    img = image_bytes_to_rgba(image_bytes)
    if img is None:
        return image_bytes

    width, height = img.size
    if width <= 2 or height <= 2:
        return encode_png(img)

    pixels = img.load()
    edge_points = []
    for x in range(width):
        edge_points.append((x, 0))
        edge_points.append((x, height - 1))
    for y in range(1, height - 1):
        edge_points.append((0, y))
        edge_points.append((width - 1, y))

    opaque_edge_colors = []
    for x, y in edge_points:
        r, g, b, a = pixels[x, y]
        if a > 0:
            opaque_edge_colors.append((r, g, b))

    if not opaque_edge_colors:
        return encode_png(img)

    quantized = Counter(
        (r // 16 * 16, g // 16 * 16, b // 16 * 16)
        for r, g, b in opaque_edge_colors
    )
    dominant_bucket, count = quantized.most_common(1)[0]
    if count / len(opaque_edge_colors) < min_edge_ratio:
        return encode_png(img)

    bucket_colors = [
        color
        for color in opaque_edge_colors
        if (
            color[0] // 16 * 16,
            color[1] // 16 * 16,
            color[2] // 16 * 16,
        )
        == dominant_bucket
    ]
    bg_color = tuple(
        int(sum(color[i] for color in bucket_colors) / len(bucket_colors))
        for i in range(3)
    )

    def close_to_background(x: int, y: int) -> bool:
        r, g, b, a = pixels[x, y]
        if a == 0:
            return True
        return max(abs(r - bg_color[0]), abs(g - bg_color[1]), abs(b - bg_color[2])) <= color_tolerance

    visited = set()
    queue = deque()
    for point in edge_points:
        if close_to_background(*point):
            queue.append(point)
            visited.add(point)

    while queue:
        x, y = queue.popleft()
        r, g, b, _ = pixels[x, y]
        pixels[x, y] = (r, g, b, 0)
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if nx < 0 or ny < 0 or nx >= width or ny >= height:
                continue
            if (nx, ny) in visited:
                continue
            if close_to_background(nx, ny):
                visited.add((nx, ny))
                queue.append((nx, ny))

    return encode_png(img)


def trim_transparent_padding(image_bytes: bytes, padding_ratio: float = 0.08) -> bytes:
    img = image_bytes_to_rgba(image_bytes)
    if img is None:
        return image_bytes
    bbox = get_alpha_bbox(img)
    if bbox is None:
        return encode_png(img)
    left, top, right, bottom = bbox
    w = right - left
    h = bottom - top
    pad_w = int(w * padding_ratio)
    pad_h = int(h * padding_ratio)
    left = max(0, left - pad_w)
    top = max(0, top - pad_h)
    right = min(img.width, right + pad_w)
    bottom = min(img.height, bottom + pad_h)
    img = img.crop((left, top, right, bottom))
    return encode_png(img)


def fit_subject_to_canvas(
    image_bytes: bytes,
    output_size: str,
    target_fill_ratio: float = 0.78,
) -> bytes:
    img = image_bytes_to_rgba(image_bytes)
    if img is None:
        return image_bytes

    try:
        cw, ch = map(int, output_size.lower().split("x"))
    except (ValueError, AttributeError):
        cw, ch = 512, 512

    bbox = get_alpha_bbox(img)
    if bbox is None:
        img = img.resize((cw, ch), Image.LANCZOS)
        return encode_png(img)

    bbox_w = bbox[2] - bbox[0]
    bbox_h = bbox[3] - bbox[1]

    if bbox_w <= 0 or bbox_h <= 0:
        img = img.resize((cw, ch), Image.LANCZOS)
        return encode_png(img)

    desired_w = cw * target_fill_ratio
    desired_h = ch * target_fill_ratio

    scale_w = desired_w / bbox_w
    scale_h = desired_h / bbox_h
    scale = min(scale_w, scale_h)

    new_w = max(1, int(img.width * scale))
    new_h = max(1, int(img.height * scale))

    img = img.resize((new_w, new_h), Image.LANCZOS)

    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    paste_x = (cw - new_w) // 2
    paste_y = (ch - new_h) // 2

    canvas.paste(img, (paste_x, paste_y), img)
    return encode_png(canvas)


def normalize_sprite_canvas(image_bytes: bytes, output_size: str) -> bytes:
    result = remove_near_white_background(image_bytes)
    result = remove_uniform_edge_background(result)
    result = trim_transparent_padding(result, padding_ratio=0.08)
    result = fit_subject_to_canvas(result, output_size)
    return result


def analyze_sprite_image(image_bytes: bytes) -> dict:
    img = image_bytes_to_rgba(image_bytes)
    if img is None:
        return {
            "width": 0,
            "height": 0,
            "has_alpha": False,
            "alpha_bbox": None,
            "subject_fill_ratio": 0.0,
            "center_offset_ratio": 1.0,
            "near_white_background_ratio": 1.0,
            "error": "cannot open image",
        }

    w, h = img.size
    bbox = get_alpha_bbox(img)

    if bbox:
        bbox_w = bbox[2] - bbox[0]
        bbox_h = bbox[3] - bbox[1]
        canvas_area = w * h
        subject_area = bbox_w * bbox_h
        subject_fill_ratio = subject_area / canvas_area if canvas_area > 0 else 0.0

        bbox_cx = bbox[0] + bbox_w / 2
        bbox_cy = bbox[1] + bbox_h / 2
        canvas_cx = w / 2
        canvas_cy = h / 2
        offset_x = abs(bbox_cx - canvas_cx) / w if w > 0 else 1.0
        offset_y = abs(bbox_cy - canvas_cy) / h if h > 0 else 1.0
        center_offset_ratio = max(offset_x, offset_y)
    else:
        subject_fill_ratio = 0.0
        center_offset_ratio = 1.0

    total = 0
    near_white_count = 0
    for r, g, b, a in img.getdata():
        total += 1
        if a > 0 and r >= 245 and g >= 245 and b >= 245:
            near_white_count += 1
    near_white_ratio = near_white_count / total if total > 0 else 0.0

    return {
        "width": w,
        "height": h,
        "has_alpha": True,
        "alpha_bbox": [bbox[0], bbox[1], bbox[2], bbox[3]] if bbox else None,
        "subject_fill_ratio": round(subject_fill_ratio, 4),
        "center_offset_ratio": round(center_offset_ratio, 4),
        "near_white_background_ratio": round(near_white_ratio, 4),
    }
