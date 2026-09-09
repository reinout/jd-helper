import subprocess
import sys
import webbrowser
from pathlib import Path

from rich import print
from rich.tree import Tree
from textual.app import App
from textual.binding import Binding
from textual.widgets import Footer, Header
from textual.widgets import Tree as TextualTree

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
                levels = _levels(area, category, id)
                output.write_id_page(id=id, levels=levels)
                output.ensure_id_dir(id=id)

                for document in id.documents:
                    output.write_document_page(document=document, id=id, levels=levels)


class JDTree(TextualTree):
    jd_structure: core.JDStructure

    BINDINGS = [
        Binding("b", "open_browser", "Open browser", show=True),
        Binding("e", "open_emacs", "Open emacs", show=True),
        Binding("f", "open_finder", "Open finder", show=True),
        # Different cursor movement to the default.
        Binding(
            "left",
            "cursor_left",
            "Ascend up the tree",
            show=False,
        ),
        Binding(
            "right",
            "cursor_right",
            "Descend into the current node",
            show=False,
        ),
    ]

    @property
    def selected_jd_item(self) -> core.Base | None:
        if self.cursor_node.data is None:
            return
        key = self.cursor_node.data.get("key")
        if not key:
            return
        return self.jd_structure.all[key]

    def action_cursor_right(self):
        # Purpose: go deeper into the structure. If the node isn't expanded, expand it.
        # And after expanding, behave as cursor-down, that descends into the now-expanded node.
        if self.cursor_node.is_collapsed:
            self.action_toggle_node()
        self.action_cursor_down()

    def action_cursor_left(self):
        # Purpose: go up into the structure and collapse what we just left.
        self.action_cursor_parent()
        self.action_toggle_node()

    def action_open_browser(self):
        if not self.selected_jd_item:
            return
        file_url = "file://" + str(output.html_path(self.selected_jd_item))
        webbrowser.open(file_url)

    def action_open_emacs(self):
        if not self.selected_jd_item:
            return
        subprocess.run(["emacsclient", "-n", str(self.selected_jd_item.path)])

    def action_open_finder(self):
        if not self.selected_jd_item:
            return
        subprocess.run(["open", str(self.selected_jd_item.path)])

    def build_tree(self):
        self.jd_structure = disk.read_folder_structure()
        self.show_root = False
        self.root.expand()
        for area_key in sorted(self.jd_structure.areas.keys()):
            area = self.jd_structure.areas[area_key]
            area_tree = self.root.add(output.rich_text(area), data={"key": area_key})
            for category_key in sorted(area.category_keys):
                category = self.jd_structure.categories[category_key]
                category_tree = area_tree.add(
                    output.rich_text(category), data={"key": category_key}
                )
                for id_key in sorted(category.id_keys):
                    id = self.jd_structure.ids[id_key]
                    category_tree.add_leaf(output.rich_text(id), data={"key": id_key})


class JDApp(App):
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
    ]

    def build_tree(self):
        tree = JDTree("JD")
        tree.build_tree()
        return tree

    def compose(self):
        yield Header()
        yield self.build_tree()
        yield Footer()


def textual_something(jd_root: Path):
    # jd_structure = disk.read_folder_structure(jd_root)
    app = JDApp()
    app.run()
