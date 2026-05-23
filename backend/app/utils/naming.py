# File and asset naming conventions
import re


def safe_filename(name: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9_\- ]", "", name)
    name = name.strip().replace(" ", "_").lower()
    name = re.sub(r"_+", "_", name)
    return name


def generate_asset_name(description: str, asset_type: str) -> str:
    base = safe_filename(description)[:30]
    return f"{asset_type}_{base}"
