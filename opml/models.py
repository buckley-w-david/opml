from __future__ import annotations

from datetime import datetime
import enum

from typing import Optional, List, Dict, Any

from dataclasses import dataclass, asdict, field

class Version(enum.Enum):
    VERSION1 = "1.0"
    VERSION11 = "1.1"
    VERSION2 = "2.0"

    @staticmethod
    def from_version(version: str):
        if version == "1.0":
            return Version.VERSION1
        elif version == "1.1":
            return Version.VERSION1
        elif version == "2.0":
            return Version.VERSION2
        raise Exception()


DOCS = {
    Version.VERSION1: "http://2005.opml.org/spec1.html",
    Version.VERSION11: "http://2005.opml.org/spec1.html",
    Version.VERSION2: "http://opml.org/spec2.opml",
}


@dataclass
class Head:
    title: Optional[str] = None
    date_created: Optional[datetime] = None
    date_modified: Optional[datetime] = None
    owner_name: Optional[str] = None
    owner_email: Optional[str] = None
    owner_id: Optional[str] = None
    docs: Optional[str] = None
    expansion_state: List[int] = field(default_factory=list)
    vert_scroll_state: Optional[int] = None
    window_top: Optional[int] = None
    window_left: Optional[int] = None
    window_bottom: Optional[int] = None
    window_right: Optional[int] = None

    def dict(self):
        return asdict(self)


@dataclass
class Outline:
    text: str
    attributes: Dict[str, Any]
    sub_outlines: List['Outline'] = field(default_factory=list)

    @staticmethod
    def rss(text: str, xml_url: str):
        return Outline(text=text, attributes={"type": "rss", "xmlUrl": xml_url})

    def dict(self):
        return asdict(self)

@dataclass
class Body:
    outlines: List[Outline]

    def dict(self):
        return asdict(self)


@dataclass
class Opml:
    version: Version
    head: Head
    body: Body

    def dict(self):
        return asdict(self)
