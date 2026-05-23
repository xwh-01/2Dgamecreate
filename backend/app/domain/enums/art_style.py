# Art style enumeration
from enum import Enum


class ArtStyle(str, Enum):
    PIXEL = "pixel"
    FLAT = "flat"
    HAND_DRAWN = "hand_drawn"
    VECTOR = "vector"
    REALISTIC = "realistic"
