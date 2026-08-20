import pytest

from jd_helper import core


@pytest.mark.parametrize(
    "number,expected",
    [
        ("10", core.Kind.AREA),
        ("12", core.Kind.CATEGORY),
        ("12.34", core.Kind.ID),
    ],
)
def test_detect_kind(number, expected):
    assert core.detect_kind(number) == expected


@pytest.mark.parametrize("number", ["100", "1", "12.", "10.23", "13.234"])
def test_detect_kind_incorrect(number):
    with pytest.raises(core.UnknownKindError):
        core.detect_kind(number)
