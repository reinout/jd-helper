from pathlib import Path

import pytest

from jd_helper import core


def test_post_init_area1():
    core.Area(number="10")


@pytest.mark.parametrize("number", ["12", "10.34", "reutel"])
def test_post_init_area2(number):
    with pytest.raises(AssertionError):
        core.Area(number=number)


def test_post_init_category1():
    core.Category(number="12")  # Smoke test


@pytest.mark.parametrize("number", ["10", "12.34", "reutel"])
def test_post_init_category2(number):
    with pytest.raises(AssertionError):
        core.Category(number=number)


def test_post_init_id1():
    core.ID(number="12.34")


@pytest.mark.parametrize("number", ["10", "12", "reutel"])
def test_post_init_id2(number):
    with pytest.raises(AssertionError):
        core.ID(number=number)


def test_build_tree():
    area = core.Area("10")
    category1 = core.Category("11")
    category2 = core.Category("12")
    id = core.ID("11.34")
    jd_structure = core.JDStructure()
    jd_structure.add_area(area)
    jd_structure.add_category(category1)
    jd_structure.add_category(category2)
    jd_structure.add_id(id)
    assert len(jd_structure.categories) == 2
    assert "12" in jd_structure.areas["10"].category_keys
    assert "11.34" in jd_structure.categories["11"].id_keys
    assert "10" in jd_structure.all
    assert "11.34" in jd_structure.all


def test_document_ordering():
    assert core.Document(Path("aaaa.md")) < core.Document(Path("zzzz.md"))


def test_document_ordering_equal():
    assert core.Document(Path("something.md")) == core.Document(Path("something.md"))


@pytest.mark.parametrize(
    "first,last",
    [
        ("aaa.pdf", "zzz,pdf"),
        ("zzz.pdf", "aaa.xls"),  # First sort on extension.
        ("zzz", "aaa.doc"),  # Dirs have no extension and are sorted first.
    ],
)
def test_file_or_folder_ordering(first, last):
    assert core.FileOrFolder(Path(first)) < core.FileOrFolder(Path(last))


def test_file_or_folder_ordering_equal():
    assert core.FileOrFolder(Path("something.doc")) == core.FileOrFolder(
        Path("something.doc")
    )


def test_base_ordering():
    assert core.Base(number="12.34") < core.Base(number="25.67")


def test_base_ordering_equal():
    assert core.Base(number="12.34") == core.Base(number="12.34")


@pytest.mark.parametrize(
    "uri", ["https://reinout.vanrees.org", "hangmap://kantoor/xyz"]
)
def test_location(uri):
    core.Pointer(uri)  # Smoke test
