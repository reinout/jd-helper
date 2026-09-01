import logging
from dataclasses import dataclass
from functools import singledispatch
from pathlib import Path
from urllib.parse import SplitResult, urlsplit

from docutils.core import publish_parts
from jinja2 import Environment, PackageLoader
from markdown_it import MarkdownIt

from jd_helper import core

JDEX_ROOT = Path("~/jdex").expanduser()

logger = logging.getLogger()
jinja_env = Environment(loader=PackageLoader("jd_helper", "templates"))

structure_page_template = jinja_env.get_template("structure_page.html")
id_page_template = jinja_env.get_template("id_page.html")
document_page_template = jinja_env.get_template("document_page.html")


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
    result = f"[link=file://{target}][bold white]:file_folder: {obj.number}[/][/] {obj.title}"
    relevant_locations = [
        rendered_link(location)
        for location in obj.locations
        if location.scheme in ("hangmap")
    ]
    if relevant_locations:
        result += f" [deep_sky_blue1](zie: {', '.join(relevant_locations)})[/]"
    return result


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
            result = f"hangmap {location}: '{label}'"
            if obj.description:
                result += f" ({obj.description}"
            return result
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
    target = html_path(obj)
    logger.debug(f"Writing {target}...")
    if obj is None:
        title = "JD"
    else:
        title = f"{obj.number} {obj.title}"
    page_meta = PageMeta(title=title, url_to_root=JDEX_ROOT)
    rendered_page = structure_page_template.render(
        levels=levels, page_meta=page_meta, links=links
    )
    target.write_text(rendered_page)


def write_id_page(id: core.ID, levels: list[Level]):
    target = html_path(id)
    logger.debug(f"Writing {target}...")
    title = f"{id.number} {id.title}"
    page_meta = PageMeta(title=title, url_to_root=JDEX_ROOT)

    locations = [rendered_link(location) for location in id.locations]
    links = [rendered_link(link) for link in id.links]
    files_and_folders = [rendered_link(ff) for ff in sorted(id.files_and_folders)]
    documents = [
        rendered_document_link(document, id.number) for document in sorted(id.documents)
    ]

    rendered_page = id_page_template.render(
        levels=levels,
        page_meta=page_meta,
        locations=locations,
        links=links,
        files_and_folders=files_and_folders,
        documents=documents,
    )
    target.write_text(rendered_page)


def ensure_id_dir(id: core.ID):
    id_dir = JDEX_ROOT / id.number
    id_dir.mkdir(exist_ok=True)


def write_document_page(document: core.Document, id: core.ID, levels: list[Level]):
    html_filename = document.path.stem + ".html"
    target = JDEX_ROOT / id.number / html_filename
    logger.debug(f"Writing {target}...")
    title = f"{id.number} → {document.title}"
    page_meta = PageMeta(title=title, url_to_root=JDEX_ROOT)

    documents = [
        rendered_document_link(document, id.number) for document in sorted(id.documents)
    ]

    # Now on to actually rendering the current document
    content = document.path.read_text(errors="replace")
    match document.path.suffix:
        case ".txt":
            lines = content.split("\n")
            rendered_content = "\n".join([f"<div>{line}</div>" for line in lines])
        case ".md":
            md = MarkdownIt("gfm-like2")
            rendered_content = md.render(content)
        case ".rst":
            parts = publish_parts(content, writer_name="html5")
            rendered_content = parts["html_body"]

    edit_link = document.path.as_uri()

    rendered_page = document_page_template.render(
        levels=levels,
        page_meta=page_meta,
        documents=documents,
        rendered_content=rendered_content,
        edit_link=edit_link,
    )
    target.write_text(rendered_page)
