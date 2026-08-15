import pytest

from jd_helper import pointers

HTTPS_URI = "https://reinout.vanrees.org/weblog/2026/08/11/managing-email.html"
HANGMAP_URI = "hangmap://thuis/layout"
HANGMAP_LINE = "hangmap://thuis/layout vooral de gele blaadjes"
BUJO_LINE = "bujo://103/78 unique output, samenvatting Naval Ravikant"
JUNK_URI = "reutel://some/where"


def test_from_uri1():
    assert str(pointers.from_uri(HANGMAP_URI)) == "hangmap thuis: 'layout'"


def test_from_uri2():
    assert type(pointers.from_uri(HTTPS_URI)) is pointers.URLPointer


def test_from_uri_junk():
    with pytest.raises(pointers.UnknownSchemeError):
        pointers.from_uri(JUNK_URI)


def test_urlpointer():
    assert str(pointers.from_uri(HTTPS_URI)) == HTTPS_URI


def test_from_line1():
    assert type(pointers.line_to_pointer(HANGMAP_LINE)) is pointers.HangmapPointer


def test_from_line2():
    result = pointers.line_to_pointer(HANGMAP_LINE)
    assert result.label == "layout"
