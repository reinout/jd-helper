import logging
from dataclasses import dataclass
from functools import singledispatch
from pathlib import Path
from urllib.parse import SplitResult, urlsplit

from jinja2 import Environment, PackageLoader

from jd_helper import core

JDEX_ROOT = Path("~/jdex").expanduser()

logger = logging.getLogger()
jinja_env = Environment(loader=PackageLoader("jd_helper", "templates"))


class UnknownSchemeError(Exception):
    pass


def html_path(obj: core.Base | None = None) -> Path:
    if obj is None:
        # Root of the site.
        return JDEX_ROOT / "index.html"
    return JDEX_ROOT / f"{obj.number}.html"


@singledispatch
def rich_text(obj: core.Base) -> str:
    return str(obj)


@rich_text.register
def _(obj: core.Area):
    target = str(html_path(obj))
    return f"[link=file://{target}][bold green]:file_cabinet:  {obj.number}[/][/] {obj.title}"


@rich_text.register
def _(obj: core.Category):
    target = str(html_path(obj))
    return f"[link=file://{target}][bold yellow]:card_file_box:  {obj.number}[/][/] {obj.title}"


@rich_text.register
def _(obj: core.ID):
    target = str(html_path(obj))
    return f"[link=file://{target}][bold white]:file_folder: {obj.number}[/][/] {obj.title}"


@singledispatch
def rendered_link(obj: core.Base) -> str:
    """Return link suitable for html"""
    # TODO: numbers as fixed width font?
    return f"<a href='{html_path(obj)}'><span class='number'>{obj.number}</span> {obj.title}</a>"


@rendered_link.register
def _(obj: core.Pointer) -> str:
    splitted: SplitResult = urlsplit(obj.uri)
    match splitted.scheme:
        case "https":
            return f"<a href='{obj.uri}'>{obj.description or 'link'}</a>"
        case "jd":
            # jd://12.34/
            number = splitted.netloc
            return f"JD '{number}'"
        case "hangmap":
            # hangmap://thuis/label-op-de-hangmap
            location = splitted.netloc
            label = splitted.path.lstrip("/")
            return f"hangmap {location}: '{label}'"
        case "bujo":
            # bujo://103/34
            number = int(splitted.netloc)
            if number >= 100:
                number -= 100
                return f"grote BuJo {number:03}"
            else:
                return f"kleine BuJo {number:03}"
        case _:
            raise UnknownSchemeError(f"Scheme {splitted.scheme} not implemented")


@rendered_link.register
def _(obj: core.FileOrFolder) -> str:
    return f"<a href='{obj.path.as_uri()}'>{obj.title}</a>"


def rendered_document_link(document: core.Document, id_number: str) -> str:
    html_filename = document.path.stem + ".html"
    target = JDEX_ROOT / id_number / html_filename
    return f"<a href='{target.as_uri()}'>{document.title}</a>"


@dataclass
class Level:
    """Level line at the top of the page, sort of breadcrumb"""

    number: str
    title: str
    url: str | Path


@dataclass
class PageMeta:
    """Generic page elements, needed for rendering."""

    title: str
    url_to_root: str | Path


def write_structure_page(obj: core.Base | None, levels: list[Level], links: list[str]):
    structure_page_template = jinja_env.get_template("structure_page.html")
    target = html_path(obj)
    logger.debug(f"Writing {target}...")
    if obj is None:
        title = "JD"
    else:
        title = f"{obj.number} {obj.title}"
    page_meta = PageMeta(title=title, url_to_root=JDEX_ROOT)
    content = structure_page_template.render(
        levels=levels, page_meta=page_meta, links=links
    )
    target.write_text(content)


def write_id_page(obj: core.ID, levels: list[Level]):
    id_page_template = jinja_env.get_template("id_page.html")
    target = html_path(obj)
    logger.debug(f"Writing {target}...")
    title = f"{obj.number} {obj.title}"
    page_meta = PageMeta(title=title, url_to_root=JDEX_ROOT)

    locations = [rendered_link(location) for location in obj.locations]
    links = [rendered_link(link) for link in obj.links]
    files_and_folders = [rendered_link(ff) for ff in sorted(obj.files_and_folders)]
    documents = [
        rendered_document_link(document, obj.number)
        for document in sorted(obj.documents)
    ]

    content = id_page_template.render(
        levels=levels,
        page_meta=page_meta,
        locations=locations,
        links=links,
        files_and_folders=files_and_folders,
        documents=documents,
    )
    target.write_text(content)
