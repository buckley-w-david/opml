import email.utils
from datetime import datetime
from pathlib import Path
from time import mktime
from typing import Any, Union, BinaryIO

from lxml import etree

from opml import models


def parse_outline(outline_node):
    attributes = {k: v for k, v in outline_node.items()}
    text = attributes.pop("text")
    sub_outlines = [
        parse_outline(suboutline_node)
        for suboutline_node in outline_node.findall("outline")
    ]
    return models.Outline(
        attributes=attributes,
        text=text,
        sub_outlines=sub_outlines,
    )

def find_text(node, element):
    result = node.xpath(f"{element}/text()")
    if result:
        return result[0]
    return None


def parse_head(head_node):
    dc = email.utils.parsedate(find_text(head_node, "dateCreated"))
    head_date_created = datetime(*dv[:7]) if dc else None

    dm = email.utils.parsedate(find_text(head_node, "dateModified"))
    head_date_modified = datetime(*dm[:7]) if dm else None

    es = find_text(head_node, "expansionState")
    expansion_state = [int(i) for i in es.split(",")] if es else []

    vss = find_text(head_node, "vertScrollState")
    vert_scroll_state = int(vss) if vss else None

    wt = find_text(head_node, "windowTop")
    window_top = int(wt) if wt else None

    wl = find_text(head_node, "windowLeft")
    window_left = int(wl) if wl else None

    wb = find_text(head_node, "windowBottom")
    window_bottom = int(wb) if wb else None

    wr = find_text(head_node, "windowRight")
    window_right = int(wr) if wr else None

    return models.Head(
        title=find_text(head_node, 'title'),
        date_created=head_date_created,
        date_modified=head_date_modified,
        owner_name=find_text(head_node, "ownerName"),
        owner_email=find_text(head_node, "ownerEmail"),
        owner_id=find_text(head_node, "ownerId"),
        docs=find_text(head_node, "docs"),
        expansion_state=expansion_state,
        vert_scroll_state=vert_scroll_state,
        window_top=window_top,
        window_left=window_left,
        window_bottom=window_bottom,
        window_right=window_right,
    )


def read(file: Union[Path, str, BinaryIO]) -> models.Opml:
    tree = etree.parse(file)

    opml_node = tree.getroot()
    version = models.Version.from_version(opml_node.get("version"))
    head_node = opml_node.find("head")

    head = parse_head(head_node)
    body_node = opml_node.find("body")
    outlines = [
        parse_outline(outline_node) for outline_node in body_node.findall("outline")
    ]

    return models.Opml(version=version, head=head, body=models.Body(outlines=outlines))
