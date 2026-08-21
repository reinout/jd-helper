from pathlib import Path

from jd_helper import disk

our_dir = Path(__file__).parent
example_root = our_dir / "example_root"


def test_number_and_title1():
    number, title = disk.number_and_title("11_something-else")
    assert number == "11"
    assert title == "something else"


def test_read_folder_structure():
    jd_structure = disk.read_folder_structure(example_root)
    assert jd_structure.categories["21"].title == "some category"
    assert "22" in jd_structure.areas["20"].category_keys
