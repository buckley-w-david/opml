from __future__ import annotations

from datetime import datetime
import enum

from typing import Optional, List, Dict, Any

from pydantic import BaseModel, EmailStr, HttpUrl


class Version(enum.Enum):
    VERSION1 = "1.0"
    VERSION11 = "1.1"
    VERSION2 = "2.0"


DOCS = {
    Version.VERSION1: "http://2005.opml.org/spec1.html",
    Version.VERSION11: "http://2005.opml.org/spec1.html",
    Version.VERSION2: "http://opml.org/spec2.opml",
}


class Head(BaseModel):
    title: Optional[str] = None
    date_created: Optional[datetime] = None
    date_modified: Optional[datetime] = None
    owner_name: Optional[str] = None
    owner_email: Optional[EmailStr] = None
    owner_id: Optional[HttpUrl] = None
    docs: Optional[HttpUrl] = None
    expansion_state: List[int] = []
    vertScrollState: Optional[int] = None
    window_top: Optional[int] = None
    window_left: Optional[int] = None
    window_bottom: Optional[int] = None
    window_right: Optional[int] = None


class Outline(BaseModel):
    sub_outlines: List[Outline] = []
    attributes: Dict[str, Any]


Outline.update_forward_refs()


class Body(BaseModel):
    outlines: List[Outline]


class Opml(BaseModel):
    version: Version
    head: Head
    body: Body
