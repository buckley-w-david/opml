import email.utils
from datetime import datetime
from pathlib import Path
from typing import Any, Union, BinaryIO

from lxml import etree

from opml.models import Opml


def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return s[0] + "".join(i.capitalize() for i in s[1:])


def convert_value(value: Any):
    if isinstance(value, list):
        return ",".join(str(i) for i in value)
    if isinstance(value, datetime):
        return email.utils.format_datetime(value)
    return str(value)


def write_outline(parent, outline):
    outline_node = etree.Element("outline")
    for k, v in outline.attributes.items():
        outline_node.set(k, convert_value(v))
    for sub_outline in outline.sub_outlines:
        write_outline(outline_node, sub_outline)
    parent.append(outline_node)


def write(file: Union[Path, str, BinaryIO], opml: Opml):
    root = etree.Element("opml", version=opml.version.value)
    head = etree.Element("head")
    for k, v in opml.head.dict().items():
        if v is not None and v != []:
            head.set(to_camel_case(k), convert_value(v))
    root.append(head)

    body = etree.Element("body")
    for outline in opml.body.outlines:
        write_outline(body, outline)
    root.append(body)

    et = etree.ElementTree(root)
    et.write(file, xml_declaration=True, encoding='UTF-8')
