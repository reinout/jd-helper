from pathlib import Path

from rich import print
from rich.tree import Tree

from jd_helper import disk, output


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
