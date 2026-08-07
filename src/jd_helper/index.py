from functools import total_ordering
from pathlib import Path

from rich import print
from rich.tree import Tree

from jd_helper import utils


@total_ordering
class Base:
    identifier: str
    number: str
    title: str
    path: Path

    def __init__(self, path: Path):
        self.path = path
        self.identifier = self.path.name
        self.number = self.identifier.split("_", 1)[0]
        self.title = self.identifier.split("_", 1)[1]

    def __str__(self) -> str:
        return self.identifier

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __lt__(self, other):
        return self.identifier < other.identifier


class ID(Base):
    pass


class Category(Base):
    ids: list[ID]


class Area(Base):
    categories: list[Category]


def read_folder_structure(jd_root: Path = utils.JD_ROOT) -> list[Area]:
    areas: list[Area] = []
    for area_path in jd_root.glob(utils.AREA_PATTERN):
        area = Area(area_path)
        categories: list[Category] = []
        for category_path in area_path.glob(utils.CATEGORY_PATTERN):
            category = Category(category_path)
            categories.append(category)
        area.categories = sorted(categories)
        areas.append(area)
    return sorted(areas)


def build_index(jd_root: Path = utils.JD_ROOT):
    """Create an index.html and other adminstrativia"""
    # First print everything.
    tree = Tree("JD index")
    areas = read_folder_structure()
    for area in areas:
        area_tree = tree.add(f"[bold green]{area.number}[/] {area.title}")
        for category in area.categories:
            area_tree.add(f"[bold yellow]{category.number}[/] {category.title}")
    print(tree)

    # Then jinja2?

    # Per categorie 00 gebruiken voor sub-bestand? Toml/json?
