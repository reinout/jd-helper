from functools import cached_property, total_ordering
from pathlib import Path

from jinja2 import Environment, PackageLoader

from jd_helper import documents, utils

jinja_env = Environment(loader=PackageLoader("jd_helper", "templates"))


@total_ordering
class Base:
    identifier: str
    number: str
    title: str
    path: Path
    parent: "Base | None"
    absolute_url_base: str

    def __init__(self, path: Path, parent: "Base | None" = None):
        self.path = path
        self.parent = parent
        self.identifier = self.path.name
        if self.identifier != "jd":
            self.number = self.identifier.split("_", 1)[0]
            self.title = self.identifier.split("_", 1)[1]
            self.title = self.title.replace("-", " ")

            if parent and parent.absolute_url_base:
                self.absolute_url_base = parent.absolute_url_base + "/" + self.number
            else:
                self.absolute_url_base = self.number

        else:
            # Root, custom case
            self.number = "JD"
            self.title = ""
            self.absolute_url_base = ""

    def __str__(self) -> str:
        return self.identifier

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __lt__(self, other):
        return self.identifier < other.identifier

    @property
    def jdex_path(self):
        return utils.JDEX_ROOT / self.absolute_url_base / "index.html"

    @property
    def as_toc_entry(self) -> utils.TocEntry:
        return utils.TocEntry(
            number=self.number,
            title=self.title,
            url=f"{self.absolute_url_base}/index.html",
        )

    @property
    def as_page(self) -> utils.Page:
        return utils.Page(
            number=self.number,
            title=self.title,
            toc_contents=self.toc_contents,
            url_to_root=self.url_to_root or ".",
            parents=self.parents,
            links=self.links,
            locations=self.locations,
            index_document=self.index_document,
        )

    @property
    def url_to_root(self) -> str:
        levels_to_root = len(self.path.relative_to(utils.JD_ROOT).parts)
        return "/".join([".."] * levels_to_root)

    @property
    def toc_contents(self) -> list[utils.TocEntry]:
        return []

    @property
    def parents(self) -> "list[Base]":
        """Return parents (for breadcrumbs), starting with the root."""
        result: list[Base] = []
        current = self.parent
        while current:
            result.append(current)
            current = current.parent
        result.reverse()
        return result

    @property
    def index_document(self) -> documents.Document | None:
        possible_index = self.path / "index.md"
        if possible_index.exists():
            return documents.MdDocument(possible_index)


class ID(Base):
    @cached_property
    def documents(self) -> list[documents.Document]:
        return documents.find_documents(self.path)

    @property
    def toc_contents(self) -> list[utils.TocEntry]:
        # Just return ourselves, in front of the documents.
        return [self.as_toc_entry]


class Category(Base):
    ids: list[ID]

    @property
    def toc_contents(self) -> list[utils.TocEntry]:
        return [id.as_toc_entry for id in self.ids]


class Area(Base):
    categories: list[Category]

    @property
    def toc_contents(self) -> list[utils.TocEntry]:
        return [category.as_toc_entry for category in self.categories]


class Root(Base):
    areas: list[Area]

    @property
    def toc_contents(self) -> list[utils.TocEntry]:
        return [area.as_toc_entry for area in self.areas]

    @property
    def as_toc_entry(self) -> utils.TocEntry:
        return utils.TocEntry(
            number=self.number,
            title=self.title,
            url="index.html",
        )


def read_folder_structure() -> Root:
    root = Root(utils.JD_ROOT)
    root.areas = []
    for area_path in utils.JD_ROOT.glob(utils.AREA_PATTERN):
        area = Area(area_path, parent=root)
        categories: list[Category] = []
        for category_path in area_path.glob(utils.CATEGORY_PATTERN):
            category = Category(category_path, parent=area)
            ids: list[ID] = []
            for id_path in category_path.glob(utils.ID_PATTERN):
                id = ID(id_path, parent=category)
                ids.append(id)
            category.ids = sorted(ids)
            categories.append(category)
        area.categories = sorted(categories)
        root.areas.append(area)
        root.areas.sort()
    return root


def build_index():
    """Create an index.html and other adminstrativia"""
    index_root = utils.JDEX_ROOT
    index_root.mkdir(exist_ok=True)
    page_template = jinja_env.get_template("page.html")
    document_template = jinja_env.get_template("document.html")

    root = read_folder_structure()
    index = index_root / "index.html"
    content = page_template.render(page=root.as_page)
    index.write_text(content)

    for area in root.areas:
        area_dir = index_root / area.number
        area_dir.mkdir(exist_ok=True)
        index = area_dir / "index.html"
        content = page_template.render(page=area.as_page)
        index.write_text(content)

        for category in area.categories:
            category_dir = area_dir / category.number
            category_dir.mkdir(exist_ok=True)
            index = category_dir / "index.html"
            content = page_template.render(page=category.as_page)
            index.write_text(content)

            for id in category.ids:
                id_dir = category_dir / id.number
                id_dir.mkdir(exist_ok=True)
                index = id_dir / "index.html"
                content = page_template.render(
                    page=id.as_page,
                    absolute_url_base=id.absolute_url_base,
                    documents=id.documents,
                    current_document=None,
                )
                index.write_text(content)

                for document in id.documents:
                    target = id_dir / document.html_filename
                    content = document_template.render(
                        page=id.as_page,
                        absolute_url_base=id.absolute_url_base,
                        documents=id.documents,
                        current_document=document,
                    )
                    target.write_text(content)
