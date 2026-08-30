import pytest

from jd_helper import core, output

HTTPS_URI = "https://reinout.vanrees.org/weblog/2026/08/11/managing-email.html"
HANGMAP_URI = "hangmap://thuis/layout"
HANGMAP_LINE = "hangmap://thuis/layout vooral de gele blaadjes"
BUJO_LINE = "bujo://103/78 unique output, samenvatting Naval Ravikant"
JUNK_URI = "reutel://some/where"


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
        (core.ID("12.34"), "/12.34.html"),
        (core.Category("12"), "/12.html"),
        (core.Area("10"), "/10.html"),
    ],
)
def test_html_path(obj, expected):
    assert str(output.html_path(obj)).endswith(expected)


@pytest.mark.parametrize(
    "pointer,expected",
    [
        (
            core.Pointer(
                "https://reinout.vanrees.org/weblog/2026/08/11/managing-email.html"
            ),
            "<a href=",
        ),
        (core.Pointer("hangmap://thuis/layout"), "hangmap thuis: 'layout'"),
        (core.Pointer("hangmap://thuis/layout", description="heel mooi"), "heel mooi"),
        (core.Pointer("bujo://103/78"), "grote BuJo 003"),
    ],
)
def test_rendered_link_pointer(pointer, expected):
    assert expected in output.rendered_link(pointer)


def test_rendered_link_pointer_faulty():
    with pytest.raises(output.UnknownSchemeError):
        output.rendered_link(core.Pointer("reutel://some/where"))
