from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jd_helper.pointers import Pointer

JD_ROOT = Path("~/jd").expanduser()
JDEX_ROOT = Path("~/jdex").expanduser()

AREA_PATTERN = "[0-9]0_*"  # J0_
CATEGORY_PATTERN = "[0-9][0-9]_*"  # JD_
ID_PATTERN = "[0-9][0-9].[0-9][0-9]_*"  # JD.ID_


@dataclass
class TocEntry:
    number: str
    title: str
    url: str  # relative


@dataclass
class FilelistingEntry:
    name: str
    description: str
    url: str  # relative


@dataclass
class Page:
    number: str
    title: str
    toc_contents: list[TocEntry]
    url_to_root: str
    parents: list
    links: list[Pointer]
    locations: list[Pointer]
