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
