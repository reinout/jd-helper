import re
from dataclasses import dataclass, field
from functools import total_ordering
from pathlib import Path

AREA_REGEX = re.compile(r"\d0")
CATEGORY_REGEX = re.compile(r"\d[1-9]")
ID_REGEX = re.compile(r"\d[1-9]\.\d\d")


@dataclass
class Location:
    uri: str
    description: str | None = None


@total_ordering
@dataclass
class Base:
    number: str
    title: str = ""
    path: Path | None = None

    def __eq__(self, other):
        return self.number == other.number

    def __lt__(self, other):
        return self.number < other.number


@dataclass
class Area(Base):
    category_keys: list[str] = field(default_factory=list)

    def __post_init__(self):
        assert AREA_REGEX.fullmatch(self.number)


@dataclass
class Category(Base):
    id_keys: list[str] = field(default_factory=list)

    def __post_init__(self):
        assert CATEGORY_REGEX.fullmatch(self.number)


@dataclass
class ID(Base):
    locations: list[Location] = field(default_factory=list)

    def __post_init__(self):
        assert ID_REGEX.fullmatch(self.number)


class JDStructure:
    areas: dict[str, Area]
    categories: dict[str, Category]
    ids: dict[str, ID]

    def __init__(self):
        self.areas = {}
        self.categories = {}
        self.ids = {}

    def add_area(self, area: Area):
        self.areas[area.number] = area

    def add_category(self, category: Category):
        self.categories[category.number] = category
        area_number = category.number[0] + "0"
        area = self.areas[area_number]
        area.category_keys.append(category.number)

    def add_id(self, id: ID):
        self.ids[id.number] = id
        category_number = id.number[:2]
        category = self.categories[category_number]
        category.id_keys.append(id.number)

    @property
    def all(self) -> dict[str, Base]:
        result: dict[str, Base] = {}
        result.update(self.areas)
        result.update(self.categories)
        result.update(self.ids)
        return result
