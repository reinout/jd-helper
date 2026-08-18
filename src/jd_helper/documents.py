import logging
from functools import cached_property, total_ordering
from pathlib import Path

from docutils.core import publish_parts
from markdown_it import MarkdownIt

SPECIAL_FILENAMES = ["links.txt", "locations.txt", "index.md"]

logger = logging.getLogger(__name__)


@total_ordering
class Document:
    title: str
    path: Path
    filename: str
    html_filename: str

    def __init__(self, path: Path):
        self.path = path
        self.filename = path.name
        self.html_filename = path.stem + ".html"
        # Temporary title, can be improved later by reading md/rst.
        self.title = self.filename

    def __eq__(self, other):
        return self.filename == other.filename

    def __lt__(self, other):
        return self.filename < other.filename

    @cached_property
    def content(self) -> str:
        return self.path.read_text(errors="replace")

    @property
    def rendered(self) -> str:
        # Default: plain text handling.
        lines = self.content.split("\n")
        return "\n".join([f"<div>{line}</div>" for line in lines])


class MdDocument(Document):
    @property
    def rendered(self):
        md = MarkdownIt("gfm-like2")
        return md.render(self.content)


class RstDocument(Document):
    @property
    def rendered(self):
        logger.debug(f"Rendering {self.path}")
        parts = publish_parts(self.content, writer_name="html5")
        return parts["html_body"]


class TxtDocument(Document):
    pass


def find_documents(path: Path) -> list[Document]:
    """Return Documents, sorted by filename"""
    result: list[Document] = []
    for extension, cls in [
        ("md", MdDocument),
        ("rst", RstDocument),
        ("txt", TxtDocument),
    ]:
        relevant_files = path.glob(f"*.{extension}")
        docs = [
            cls(relevant_file)
            for relevant_file in relevant_files
            if relevant_file.name not in SPECIAL_FILENAMES
        ]
        result += docs
    result.sort()
    return result
