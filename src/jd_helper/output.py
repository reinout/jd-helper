import logging
from dataclasses import dataclass
from functools import singledispatch
from pathlib import Path

from jinja2 import Environment, PackageLoader

from jd_helper import core, pointers

JDEX_ROOT = Path("~/jdex").expanduser()

logger = logging.getLogger()
jinja_env = Environment(loader=PackageLoader("jd_helper", "templates"))


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
def link(obj: core.Base) -> str:
    """Return link suitable for html"""
    # TODO: numbers as fixed width font?
    return f"<a href='{html_path(obj)}'><span class='number'>{obj.number}</span> {obj.title}</a>"


@link.register
def _(obj: core.Location) -> str:
    pointer = pointers.from_uri(uri=obj.uri, description=obj.description)
    return pointer.link


@dataclass
class Level:
    """Level line at the top of the page, sort of breadcrumb"""

    number: str
    title: str
    url: str | Path


@dataclass
class PageMeta:
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

    locations = [link(location) for location in obj.locations]

    content = id_page_template.render(
        levels=levels, page_meta=page_meta, locations=locations
    )
    target.write_text(content)
