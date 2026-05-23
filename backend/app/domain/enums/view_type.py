# View type enumeration (isometric, top-down, side-scroller, etc.)
from enum import Enum


class ViewType(str, Enum):
    TOP_DOWN = "top_down"
    SIDE_SCROLLER = "side_scroller"
    ISOMETRIC = "isometric"
    FIRST_PERSON = "first_person"
