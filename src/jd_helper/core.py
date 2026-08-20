import re
from dataclasses import dataclass, field
from enum import Enum

AREA_REGEX = re.compile(r"\d0")
CATEGORY_REGEX = re.compile(r"\d[1-9]")
ID_REGEX = re.compile(r"\d[1-9]\.\d\d")


class UnknownKindError(Exception):
    pass


class Kind(Enum):
    AREA = 1
    CATEGORY = 2
    ID = 3


def detect_kind(number: str) -> Kind:
    if AREA_REGEX.fullmatch(number):
        return Kind.AREA
    if CATEGORY_REGEX.fullmatch(number):
        return Kind.CATEGORY
    if ID_REGEX.fullmatch(number):
        return Kind.ID
    raise UnknownKindError(f"Number {number} not detected as JD item")


@dataclass
class JDItem:
    number: str
    title: str = ""
    kind: Kind = field(init=False)

    def __post_init__(self):
        self.kind = detect_kind(self.number)


class JDStructure:
    areas: dict[str, JDItem]
    categories: dict[str, JDItem]
    ids: dict[str, JDItem]

    def __init__(self):
        self.areas = {}
        self.categories = {}
        self.ids = {}

    def add_jd_item(self, jd_item: JDItem):
        match jd_item.kind:
            case Kind.AREA:
                self.areas[jd_item.number] = jd_item
            case Kind.CATEGORY:
                self.categories[jd_item.number] = jd_item
            case Kind.ID:
                self.ids[jd_item.number] = jd_item
