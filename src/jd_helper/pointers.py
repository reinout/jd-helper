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


@register_schemes
class URLPointer(Pointer):
    schemes = ["https"]

    def __str__(self):
        return self.uri


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


def from_uri(uri, description: str | None = None) -> Pointer:
    scheme, rest = uri.split("://")
    if scheme not in scheme_registry:
        raise UnknownSchemeError(f"Scheme {scheme} not registered")
    cls = scheme_registry[scheme]
    return cls(uri, description)


def line_to_pointer(line: str) -> Pointer:
    if " " in line:
        uri, description = line.split(" ", 1)
        return from_uri(uri, description)
    else:
        return from_uri(line)
