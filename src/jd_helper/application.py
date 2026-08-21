import sys
from pathlib import Path

from rich import print
from rich.tree import Tree

from jd_helper import core, disk, output


def print_index_to_console(jd_root: Path, selected: str | None = None):
    # Calling "Tree" and "print" should really happen in output.py, but the tree
    # structure is really part of the application...
    jd_structure = disk.read_folder_structure(jd_root)
    for area_key in sorted(jd_structure.areas.keys()):
        area = jd_structure.areas[area_key]
        area_tree = Tree(output.rich_text(area))
        for category_key in sorted(area.category_keys):
            category = jd_structure.categories[category_key]
            category_tree = area_tree.add(output.rich_text(category))
            if selected and selected in [area_key, category_key]:
                for id_key in sorted(category.id_keys):
                    id = jd_structure.ids[id_key]
                    category_tree.add(output.rich_text(id))
        print(area_tree)


def print_cd_into_dir(jd_root: Path, number: str):
    jd_structure = disk.read_folder_structure(jd_root)
    all: dict[str, core.Base] = {}
    all.update(jd_structure.areas)
    all.update(jd_structure.categories)
    all.update(jd_structure.ids)
    if number not in all:
        print(f"An area/category/id with number {number} was not found")
        sys.exit(1)
    found = all[number]
    print(f"cd {found.path}")
    print(f"mc {found.path}")
