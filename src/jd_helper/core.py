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
class Document:
    path: Path
    title: str = ""

    def __eq__(self, other):
        return self.path.name == other.path.name

    def __lt__(self, other):
        return self.path.name < other.path.name


@total_ordering
@dataclass
class FileOrFolder:
    path: Path
    title: str = ""
    extension: str = ""

    def __post_init__(self):
        if not self.title:
            self.title = self.path.name
        self.extension = self.path.suffix

    def __eq__(self, other):
        return self.path.name == other.path.name

    def __lt__(self, other):
        test1 = self.extension < other.extension
        if test1:
            return test1
        return self.path.name < other.path.name


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
    """
    The ID actually has contents. And alternative locations ("hangmap") admin.

    - Locations are found in location.txt files.
    - Documents are md/rst/txt files that we want to render and display.
    - Files and folders are just clickable. Should be grouped by extension (or by
      type=folder). Images might be shown in a more friendly way, but that's outside of
      core's purview.

    Note: there are no .add_document()-like methods, these can just be added by other
    code as they're just a list.

    """

    locations: list[Location] = field(default_factory=list)
    documents: list[Document] = field(default_factory=list)
    files_and_folders: list[FileOrFolder] = field(default_factory=list)

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
