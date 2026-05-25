# AI 2D Game Asset Generator

A tool for generating 2D game assets (characters, items, tiles, UI icons) using AI image generation models. Generated assets are production-ready for Unity and Godot.

## Requirements

- Python 3.10+
- OpenAI API key (for image generation, DALL-E 3)
- DeepSeek API key (for requirement parsing, optional falls back to OpenAI)

## Installation

```bash
cd backend
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the `backend/` directory:

```env
IMAGE_PROVIDER=openai
IMAGE_API_KEY=sk-your-openai-api-key
IMAGE_MODEL=dall-e-3
DEEPSEEK_API_KEY=sk-your-deepseek-key
DEEPSEEK_MODEL=deepseek-chat
```

| Variable | Description | Example |
|----------|-------------|---------|
| `IMAGE_PROVIDER` | Image generation provider | `openai` |
| `IMAGE_API_KEY` | OpenAI key for DALL-E image generation | `sk-...` |
| `IMAGE_MODEL` | DALL-E model | `dall-e-3` |
| `DEEPSEEK_API_KEY` | DeepSeek key for requirement parsing | `sk-...` |
| `DEEPSEEK_MODEL` | DeepSeek chat model | `deepseek-chat` |

> If `DEEPSEEK_API_KEY` is not set, requirement parsing falls back to OpenAI GPT-3.5-turbo using `IMAGE_API_KEY`.

## Running

```bash
cd backend
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 in your browser.

## Usage

1. **Create Project** — Enter a project name and description, click "Create Project"
2. **Configure Style** — Set art style (pixel art / cartoon / hand drawn), view type, color palette, default size, and prompt rules
3. **Generate Asset** — Select asset type (character / item / tile / UI icon), describe what you want, set size and direction, then click "Generate Asset"
4. **View Assets** — See all generated assets in the Assets tab, preview images, and download

## Why generation fails without IMAGE_API_KEY

If `IMAGE_API_KEY` is not configured or is empty, the system returns an explicit error:

```
image provider is not configured
```

This is intentional. The tool requires a real AI image generation API to produce assets. No mock or placeholder images are used.

## Structured asset controls

The requirement parser now extracts fine-grained control fields from user descriptions, giving you precise control over generated sprites:

| Field | Description | Suggested values |
|-------|-------------|-----------------|
| `pose` | Character stance | `idle`, `walking`, `attacking`, `casting`, `hurt`, `dead` |
| `camera_angle` | Viewpoint direction | `front`, `side`, `back`, `three-quarter`, `top-down` |
| `body_ratio` | Body proportions | `chibi`, `realistic`, `1:1`, `1:2` |
| `canvas_fill` | Subject fill ratio | `60%`, `75%`, `85%` |
| `outline_style` | Line art style | `clean`, `sketchy`, `none`, `thick`, `thin` |
| `color_palette` | Color scheme | `pastel`, `dark`, `vibrant`, `monochrome`, `warm`, `cool` |
| `emotion` | Subject expression | `neutral`, `angry`, `happy`, `sad`, `fierce`, `calm` |
| `complexity` | Detail level | `simple`, `medium`, `detailed` |
| `animation_frame` | Sprite sheet frame | `idle_1`, `walk_3`, etc. |
| `forbidden_elements` | Excluded items | `["text", "watermark", "white background", "complex scene"]` |

Example:
```json
{
  "subject": "fire mage",
  "pose": "casting",
  "camera_angle": "three-quarter",
  "canvas_fill": "85%",
  "emotion": "fierce",
  "color_palette": "warm",
  "complexity": "detailed"
}
```

### Asset type prompt templates

Each asset type uses a dedicated template injected into the generation prompt:

- **Character / Enemy**: single subject, full body, centered, transparent alpha background, subject occupies 75-85% of canvas, no white rectangle/box, no scene background, clean silhouette, Unity/Godot sprite import ready
- **Prop / Item**: single item, centered, transparent background, no ground shadow, inventory-ready icon
- **Tile**: top-down orthographic view, edge-matchable, seamless repeatable (when requested), no perspective distortion
- **UI Icon**: centered, transparent background, high contrast, simple readable shape, minimal design
- **Effect / VFX**: transparent background, centered, high contrast, particle or energy style, game-ready sprite sheet frame

### Negative prompt

All generations include a comprehensive negative prompt that excludes:
- text, watermark, logo, signature
- white background, white square, white rectangle, white box, white frame
- border, frame, cropped body, partial body
- tiny character, far away, zoomed out
- multiple characters, group, crowd
- environment background, complex scene, landscape, room
- realistic photo, realistic render, 3D render, plastic toy, smooth gradient

## Sprite Post-processing & Quality Check

Every generated asset automatically goes through a post-processing pipeline and quality assessment to ensure it is game-ready for Unity and Godot 2D sprite import:

### Post-processing pipeline

1. **White background removal** — Detects and removes near-white pixels (RGB >= 245 on all channels) by setting alpha to 0
2. **Transparent PNG conversion** — Ensures all outputs are RGBA PNG with proper alpha channel
3. **Padding trimming** — Crops excess transparent padding around the subject, leaving a small 8% margin
4. **Subject centering** — Centers the visible subject on the canvas
5. **Canvas fitting** — Scales the subject so it occupies approximately 75-85% of the output canvas

If any step fails, the pipeline falls back to the unprocessed image and logs a warning — task generation does not fail.

### Quality checks (non-blocking)

Each processed image is analyzed for sprite readiness:

| Check | Threshold | Purpose |
|-------|-----------|---------|
| `transparent_background` | Alpha channel present | Ensures RGBA format |
| `subject_fill_ratio` | >= 0.55 | Warns if subject is too small on canvas |
| `centered_subject` | offset <= 0.18 | Warns if subject is off-center |
| `near_white_background` | ratio <= 0.25 | Warns if white background remnants remain |

These checks produce warnings in `overall_message` but do **not** fail the task. Critical checks (`image_exists`, `is_png`, `file_size`) remain the only blocking validations.

### Test the pipeline

```bash
cd backend
python scripts/test_image_postprocess.py
```

Creates a white-background test image with a red square, runs normalization, and prints before/after analysis.

## Structured Asset Generation UI

The web interface provides a structured generation panel that controls every aspect of the generated sprite through form fields rather than free-form text alone:

### Asset type selector

Click one of the type buttons to switch between **Character**, **Enemy**, **Item**, **Tile**, **UI Icon**, and **Effect**. The form fields change dynamically per type.

### Structured controls per asset type

| Control | Types | Description | Values |
|---------|-------|-------------|--------|
| Name | All | Subject identifier | Text input |
| View | Character, Enemy | Camera angle | front / side / back / top-down / three-quarter |
| Pose | Character, Enemy | Action pose | idle / walking / attacking / casting / hurt / dead |
| Emotion | Character, Enemy | Expression | cute / angry / serious / crazy / happy / sad |
| Appearance | All | Visual details | Text area |
| Weapon | Character, Enemy | Held item | Text input |
| Canvas Fill | All | Subject size on canvas | 60% / 75% / 85% |
| Complexity | All | Detail level | simple / medium / detailed |
| Color Palette | All | Main color scheme | Text input (e.g. "red, black, gold") |
| Outline Style | Character, Enemy, Item | Line art | clean / bold / thin / pixel / none |
| Background | Character, Enemy | BG type | transparent / solid |
| Category | Item | Item type | weapon / potion / coin / key / food / gem |
| Tile Type | Tile | Terrain type | floor / wall / grass / water / lava / road |
| Material | Tile | Texture | Text input |
| Seamless | Tile | Tiling | yes / no |
| Purpose | UI Icon | Function | health / coin / skill / inventory / settings / map |
| Shape | UI Icon | Frame | circle / square / diamond / no_frame |
| Effect Type | Effect | Element | fire / ice / lightning / healing / explosion / poison / shield |
| Motion | Effect | Movement | burst / spiral / slash / aura / trail / flicker |
| Size | All | Output resolution | 32x32 / 64x64 / 128x128 / 256x256 / 512x512 |

### Quick templates

Five default templates at the top for instant fill:
- **Pixel demon** enemy (pixel art red demon)
- **Chibi mage** character (Q-style blue mage)
- **Coin** item (gold coin icon)
- **Grass** tile (seamless grass terrain)
- **Fireball** effect (flame burst VFX)

### Two-column layout

- **Left column**: structured form with type selector, all parameter fields, tag chips, generate button, and collapsible prompt preview
- **Right column**: sticky preview panel with checkerboard background (for transparent PNG visibility), progress steps, quality check results, and result actions (download, copy, regenerate, modify, quick optimize)

### Quality check display

After generation, the preview panel shows non-blocking quality metrics from the backend:
- **Transparent background** — alpha channel presence
- **Subject fill ratio** — warns if < 55%
- **Centered subject** — warns if offset > 18%
- **Near white background** — warns if > 25% residue

Passed checks show as green checkmarks; warnings show as yellow alerts. These never block generation.

## Testing

```bash
cd backend
python -m compileall app
```

## Project Structure

```
backend/
  app/
    ai/              # AI integration (parser, prompt builder, generator)
    api/             # FastAPI routes
    data/            # JSON file storage (auto-created)
    db/              # Database session (JSON-backed)
    domain/          # Domain entities and enums
    repositories/    # Data access layer
    schemas/         # Pydantic request/response schemas
    services/        # Business logic
    storage/         # File system storage
    utils/           # Image, naming, time utilities
    workflows/       # Asset generation pipeline
  generated_assets/  # Generated image files
  requirements.txt
```
