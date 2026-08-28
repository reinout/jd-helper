# Schemes = https, hangmap, tijdschrift

# Pointer is something that I can render. Either as a link or as a "look in this file
# folder". Including an icon, if handy.

# I also want to read/generate them from lines in links.txt and locations.txt.
from __future__ import annotations

from urllib.parse import SplitResult, urlsplit


class UnknownSchemeError(Exception):
    pass


scheme_registry: dict[str, Pointer] = {}


def register_schemes(cls):
    for scheme in cls.schemes:
        scheme_registry[scheme] = cls
    return cls


class Pointer:
    schemes: list[str] = []
    splitted: SplitResult

    def __init__(self, uri: str, description: str | None = None):
        self.uri = uri
        self.description = description
        self.splitted = urlsplit(uri)
        assert self.splitted.scheme in self.schemes

    def __str__(self):
        return self.uri

    @property
    def link(self) -> str:
        """Return link, suitable for html"""
        return str(self)


@register_schemes
class URLPointer(Pointer):
    schemes = ["https"]

    @property
    def link(self) -> str:
        """Return link, suitable for html"""
        return f"<a href='{self.uri}'>{self.description or 'link'}</a>"


@register_schemes
class JdPointer(Pointer):
    schemes = ["jd"]

    @property
    def number(self) -> str:
        return self.splitted.netloc

    # TODO: link, but that depends on index.py's find_number()... Chicken/egg.

    def __str__(self):
        return f"JD '{self.number}'"


@register_schemes
class HangmapPointer(Pointer):
    schemes = ["hangmap"]

    @property
    def location(self):
        return self.splitted.netloc

    @property
    def label(self):
        return self.splitted.path.lstrip("/")

    def __str__(self):
        return f"hangmap {self.location}: '{self.label}'"


@register_schemes
class BujoPointer(Pointer):
    schemes = ["bujo"]

    @property
    def location(self):
        number = int(self.splitted.netloc)
        if number >= 100:
            number -= 100
            return f"grote BuJo {number:03}"
        else:
            return f"kleine BuJo {number:03}"

    @property
    def page_number(self):
        return self.splitted.path.lstrip("/")

    def __str__(self):
        return f"{self.location}: pagina {self.page_number}"


def from_uri(uri, description: str | None = None) -> Pointer:
    scheme, rest = uri.split("://")
    if scheme not in scheme_registry:
        raise UnknownSchemeError(f"Scheme {scheme} not registered")
    cls = scheme_registry[scheme]
    return cls(uri, description)
