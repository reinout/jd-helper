from functools import singledispatch
from pathlib import Path

from jd_helper import core

JDEX_ROOT = Path("~/jdex").expanduser()


@singledispatch
def html_path(obj: core.Base) -> Path:
    return JDEX_ROOT / f"{obj.number}.html"


@html_path.register
def _(obj: core.ID):
    return JDEX_ROOT / obj.number / "index.html"


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
