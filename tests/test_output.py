import pytest

from jd_helper import core, output


@pytest.mark.parametrize(
    "obj,expected",
    [
        (core.ID("12.34"), "file_folder"),
        (core.Category("12"), "file_box"),
        (core.Area("10"), "file_cabinet"),
    ],
)
def test_rich_text(obj, expected):
    assert expected in output.rich_text(obj)


@pytest.mark.parametrize(
    "obj,expected",
    [
        (core.ID("12.34"), "/12.34/index.html"),
        (core.Category("12"), "/12.html"),
        (core.Area("10"), "/10.html"),
    ],
)
def test_html_path(obj, expected):
    assert str(output.html_path(obj)).endswith(expected)
