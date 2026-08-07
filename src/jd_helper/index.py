import argparse
import sys
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
        self.title = self.title.replace("-", " ")

    def __str__(self) -> str:
        return self.identifier

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __lt__(self, other):
        return self.identifier < other.identifier

    @property
    def rich_text(self):
        return str(self)


class ID(Base):
    @property
    def rich_text(self):
        return f"[link=file://{self.path}][bold white]:file_folder: {self.number}[/][/] {self.title}"


class Category(Base):
    ids: list[ID]

    @property
    def rich_text(self):
        return f"[link=file://{self.path}][bold yellow]:card_file_box:  {self.number}[/][/] {self.title}"


class Area(Base):
    categories: list[Category]

    @property
    def rich_text(self):
        return f"[link=file://{self.path}][bold green]:file_cabinet:  {self.number}[/][/] {self.title}"


def read_folder_structure(jd_root: Path = utils.JD_ROOT) -> list[Area]:
    areas: list[Area] = []
    for area_path in jd_root.glob(utils.AREA_PATTERN):
        area = Area(area_path)
        categories: list[Category] = []
        for category_path in area_path.glob(utils.CATEGORY_PATTERN):
            category = Category(category_path)
            ids: list[ID] = []
            for id_path in category_path.glob(utils.ID_PATTERN):
                id = ID(id_path)
                ids.append(id)
            category.ids = sorted(ids)
            categories.append(category)
        area.categories = sorted(categories)
        areas.append(area)
    return sorted(areas)


def build_index(jd_root: Path = utils.JD_ROOT):
    """Create an index.html and other adminstrativia"""
    pass


def print_index(jd_root: Path = utils.JD_ROOT):
    """Create an index.html and other adminstrativia"""
    selected: str | None = None
    if len(sys.argv) > 1:
        selected = sys.argv[1]
    areas = read_folder_structure(jd_root)
    for area in areas:
        area_tree = Tree(area.rich_text)
        for category in area.categories:
            category_tree = area_tree.add(category.rich_text)
            if selected and selected == category.number:
                for id in category.ids:
                    category_tree.add(id.rich_text)
        print(area_tree)


def find_number(number: str, jd_root: Path = utils.JD_ROOT) -> Base | None:
    for area in read_folder_structure(jd_root):
        if area.number == number:
            return area
        for category in area.categories:
            if category.number == number:
                return category
            for id in category.ids:
                if id.number == number:
                    return id


def cd_into_dir(jd_root: Path = utils.JD_ROOT):
    """cd into area, category or id"""
    parser = argparse.ArgumentParser(prog="jdcd")
    parser.add_argument("number")
    args = parser.parse_args(sys.argv[1:])
    found = find_number(args.number, jd_root)
    if not found:
        print(f"An area/category/id with number {args.number} was not found")
        sys.exit(1)
    print(f"cd {found.path}")
