import pytest

from jd_helper import core


def test_post_init_area1():
    core.Area(number="10")


@pytest.mark.parametrize("number", ["12", "10.34", "reutel"])
def test_post_init_area2(number):
    with pytest.raises(AssertionError):
        core.Area(number=number)


def test_post_init_category1():
    core.Category(number="12")


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


@pytest.mark.parametrize(
    "uri", ["https://reinout.vanrees.org", "hangmap://kantoor/xyz"]
)
def test_location(uri):
    core.Pointer(uri)
