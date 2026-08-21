from pathlib import Path

import pytest

from jd_helper import disk

our_dir = Path(__file__).parent
example_root = our_dir / "example_root"


def test_number_and_title1():
    number, title = disk.number_and_title("11_something-else")
    assert number == "11"
    assert title == "something else"


def test_read_folder_structure():
    # Not really a unit test :-)
    jd_structure = disk.read_folder_structure(example_root)
    assert jd_structure.categories["21"].title == "some category"
    assert "22" in jd_structure.areas["20"].category_keys


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
