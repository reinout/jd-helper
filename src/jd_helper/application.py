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
    if number not in jd_structure.all:
        print(f"An area/category/id with number {number} was not found")
        sys.exit(1)
    found = jd_structure.all[number]
    print(f"cd {found.path}")
    print(f"mc {found.path}")


def _levels(*acids: core.Base) -> list[output.Level]:
    result: list[output.Level] = []
    result.append(output.Level(url=output.html_path(), number="JDEX", title=""))
    for acid in acids:
        result.append(
            output.Level(
                url=output.html_path(acid), number=acid.number, title=acid.title
            )
        )
    return result


def export_html_pages(jd_root: Path):
    """Export the structure and the documents as html."""
    jd_structure = disk.read_folder_structure(jd_root)

    # index (list areas), root means obj=None
    areas = sorted(jd_structure.areas.values())
    levels = _levels()
    links = [output.rendered_link(area) for area in areas]
    output.write_structure_page(obj=None, levels=levels, links=links)

    # area (list categories)
    for area in areas:
        categories = [
            jd_structure.categories[category_key]
            for category_key in sorted(area.category_keys)
        ]
        levels = _levels(area)
        links = [output.rendered_link(category) for category in categories]
        output.write_structure_page(obj=area, levels=levels, links=links)

        for category in categories:
            ids = [jd_structure.ids[id_key] for id_key in sorted(category.id_keys)]
            levels = _levels(area, category)
            links = [output.rendered_link(id) for id in ids]
            # TODO: rename to toc_items and leave .link to output
            output.write_structure_page(obj=category, levels=levels, links=links)

            for id in ids:
                output.write_id_page(obj=id, levels=levels)

    # id (content overview)
    # + content items
