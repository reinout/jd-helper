from pathlib import Path

from jd_helper import core

AREA_PATTERN = "[0-9]0_*"  # J0_
CATEGORY_PATTERN = "[0-9][0-9]_*"  # JD_
ID_PATTERN = "[0-9][0-9].[0-9][0-9]_*"  # JD.ID_


def number_and_title(dirname: str) -> tuple[str, str]:
    number = dirname.split("_", 1)[0]
    title = dirname.split("_", 1)[1]
    title = title.replace("-", " ")
    return number, title


def read_folder_structure(root: Path) -> core.JDStructure:
    jd_structure = core.JDStructure()

    for area_path in root.glob(AREA_PATTERN):
        number, title = number_and_title(area_path.name)
        area = core.Area(number=number, title=title, path=area_path)
        jd_structure.add_area(area)

        for category_path in area_path.glob(CATEGORY_PATTERN):
            number, title = number_and_title(category_path.name)
            category = core.Category(number=number, title=title, path=category_path)
            jd_structure.add_category(category)

            for id_path in category_path.glob(ID_PATTERN):
                number, title = number_and_title(id_path.name)
                id = core.ID(number=number, title=title, path=id_path)
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
