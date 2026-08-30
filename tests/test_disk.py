from pathlib import Path

import pytest

from jd_helper import disk

our_dir = Path(__file__).parent
example_root = our_dir / "example_root"


def test_area_pattern(tmp_path: Path):
    dir1 = tmp_path / "40_correct-name"
    dir2 = tmp_path / "50-wrong-dash-instead-of-underscore"
    dir3 = tmp_path / "62_wrong-not-a-multiple-of-ten"
    dir4 = tmp_path / "70.34_wrong-is-an-ID"
    dir1.mkdir()
    dir2.mkdir()
    dir3.mkdir()
    dir4.mkdir()
    assert len(list(tmp_path.glob(disk.AREA_PATTERN))) == 1


def test_category_pattern(tmp_path: Path):
    dir1 = tmp_path / "40_correct-name-zero-allowed"
    dir2 = tmp_path / "50-wrong-dash-instead-of-underscore"
    dir3 = tmp_path / "62_also-correct-name"
    dir4 = tmp_path / "70.34_wrong-is-an-ID"
    dir1.mkdir()
    dir2.mkdir()
    dir3.mkdir()
    dir4.mkdir()
    assert len(list(tmp_path.glob(disk.CATEGORY_PATTERN))) == 2


def test_id_pattern(tmp_path: Path):
    dir1 = tmp_path / "40_wrong-is-area"
    dir2 = tmp_path / "51.23-wrong-dash-instead-of-underscore"
    dir3 = tmp_path / "62_wrong-is-category"
    dir4 = tmp_path / "72.34_correct"
    dir1.mkdir()
    dir2.mkdir()
    dir3.mkdir()
    dir4.mkdir()
    assert len(list(tmp_path.glob(disk.ID_PATTERN))) == 1


def test_number_and_title1():
    number, title = disk.number_and_title("11_something-else")
    assert number == "11"
    assert title == "something else"


def test_read_folder_structure():
    # Not really a unit test :-)
    jd_structure = disk.read_folder_structure(example_root)
    assert jd_structure.categories["21"].title == "some category"
    assert "22" in jd_structure.areas["20"].category_keys


def test_find_documents():
    our_root_dir = Path(__file__).parent.parent
    # We have a readme and a changelog.
    docs = disk.find_documents(our_root_dir)
    assert len(docs) == 2
    assert sorted(docs)[1].title == "jd-helper"  # Title of the readme.


@pytest.mark.parametrize(
    "line,uri,title",
    [
        ("https://reinout.vanrees.org hoera", "https://reinout.vanrees.org", "hoera"),
        ("https://reinout.vanrees.org", "https://reinout.vanrees.org", None),
    ],
)
def test_uri_and_title_from_line1(line, uri, title):
    assert disk.uri_and_title_from_line(line) == (uri, title)


def test_uris_and_titles_from_file_nonexisting():
    assert disk.uris_and_titles_from_file(Path("does-not-exist.txt")) == []


def test_uris_and_titles_from_file():
    assert disk.uris_and_titles_from_file(
        example_root / "20_second-area/21_some-category/21.10_an-id/locations.txt"
    ) == [("hangmap://thuis/a-folder", None)]
