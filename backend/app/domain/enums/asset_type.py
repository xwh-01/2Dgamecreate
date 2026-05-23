# Asset type enumeration
from enum import Enum


class AssetType(str, Enum):
    CHARACTER = "character"
    PROP = "prop"
    TILE = "tile"
    UI_ICON = "ui_icon"
    EFFECT = "effect"
