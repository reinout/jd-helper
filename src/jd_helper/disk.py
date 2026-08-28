import logging
from pathlib import Path

from jd_helper import core

AREA_PATTERN = "[0-9]0_*"  # J0_
CATEGORY_PATTERN = "[0-9][0-9]_*"  # JD_
ID_PATTERN = "[0-9][0-9].[0-9][0-9]_*"  # JD.ID_

logger = logging.getLogger(__name__)


def number_and_title(dirname: str) -> tuple[str, str]:
    number = dirname.split("_", 1)[0]
    title = dirname.split("_", 1)[1]
    title = title.replace("-", " ")
    return number, title


def read_folder_structure(root: Path) -> core.JDStructure:
    logger.debug(f"Reading folder structure from {root}...")
    jd_structure = core.JDStructure()

    for area_path in root.glob(AREA_PATTERN):
        number, title = number_and_title(area_path.name)
        logger.debug(f"Adding {number}...")
        area = core.Area(number=number, title=title, path=area_path)
        jd_structure.add_area(area)

        for category_path in area_path.glob(CATEGORY_PATTERN):
            number, title = number_and_title(category_path.name)
            logger.debug(f"Adding {number}...")
            category = core.Category(number=number, title=title, path=category_path)
            jd_structure.add_category(category)

            for id_path in category_path.glob(ID_PATTERN):
                number, title = number_and_title(id_path.name)
                logger.debug(f"Adding {number}...")
                id = core.ID(number=number, title=title, path=id_path)
                # Read ID's contents
                id.files_and_folders = find_files_and_folders(id_path)
                id.locations = find_locations(id_path)
                # TODO: documents
                jd_structure.add_id(id)

    return jd_structure


def uri_and_title_from_line(line: str) -> tuple[str, str | None]:
    if " " in line:
        uri, title = line.split(" ", 1)
        return uri, title
    else:
        return line, None


def uris_and_titles_from_file(uri_file: Path) -> list[tuple[str, str | None]]:
    """Return pointers from file. Ok if file doesn't exist."""
    if not uri_file.exists():
        return []
    lines = uri_file.read_text().split("\n")
    return [uri_and_title_from_line(line) for line in lines if line.strip()]


def find_files_and_folders(path: Path) -> list[core.FileOrFolder]:
    """Return files and folders (direct children only)"""
    logger.debug(f"Finding files and folders in {path}...")
    result: list[core.FileOrFolder] = []
    relevant_extensions = [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".odt", ".pages"]
    # Perhaps only exclude stuff, like md/rst/txt?

    for item in path.iterdir():
        if item.is_dir():
            result.append(core.FileOrFolder(path=item))
            continue
        elif item.suffix in relevant_extensions:
            result.append(core.FileOrFolder(path=item))
        else:
            logger.debug(f"Skipped file {item}")

    return result


def _line_to_location(line: str) -> core.Location:
    if " " in line:
        uri, name = line.split(" ", 1)
        return core.Location(uri=uri)
    else:
        return core.Location(uri=uri, description=name)


def find_locations(id_path: Path) -> list[core.Location]:
    """Return locations from locations.txt. Ok if file doesn't exist."""
    locations_file = id_path / "locations.txt"
    if not locations_file.exists():
        return []
    lines = locations_file.read_text().split("\n")
    return [_line_to_location(line) for line in lines if line.strip()]
