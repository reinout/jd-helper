from functools import cached_property, total_ordering
from pathlib import Path


@total_ordering
class FolderFileBase:
    path: Path
    filename: str

    def __init__(self, path: Path):
        self.path = path
        self.filename = path.name

    @cached_property
    def extension(self) -> str:
        return ""  # Not useful for folders

    def __eq__(self, other):
        return self.filename == other.filename

    def __lt__(self, other):
        test1 = self.extension < other.extension
        if test1:
            return test1
        return self.filename < other.filename

    @property
    def link(self) -> str:
        """Return rendered link for use in a <li>."""
        # TODO icon or so?
        return f"<a href='{self.path.as_uri()}'>{self.filename}</a>"


class Folder(FolderFileBase):
    pass


class File(FolderFileBase):
    @cached_property
    def extension(self) -> str:
        return self.path.suffix


def find_folders(path: Path) -> list[Folder]:
    """Return folders, sorted by filename"""
    result = [Folder(child) for child in path.iterdir() if child.is_dir()]
    result.sort()
    return result


def find_files(path: Path) -> list[File]:
    """Return files, sorted by filename"""
    print(f"Finding files in {path}...")
    result: list[File] = []
    extensions = ["jpg", "jpeg", "png", "gif", "pdf"]
    for extension in extensions:
        relevant_files = path.glob(f"*.{extension}")
        files = [File(relevant_file) for relevant_file in relevant_files]
        result += files
    result.sort()
    print(result)
    return result
