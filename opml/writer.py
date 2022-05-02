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
    outline_node = etree.SubElement(parent, "outline")

    outline_node.set('text', outline.text)
    for k, v in outline.attributes.items():
        outline_node.set(k, convert_value(v))
    for sub_outline in outline.sub_outlines:
        write_outline(outline_node, sub_outline)
    parent.append(outline_node)

def serialize(opml: Opml):
    root = etree.Element("opml", version=opml.version.value)
    head = etree.SubElement(root, "head")
    for k, v in opml.head.dict().items():
        if v is not None and v != []:
            etree.SubElement(head, to_camel_case(k)).text = convert_value(v)

    body = etree.SubElement(root, "body")
    for outline in opml.body.outlines:
        write_outline(body, outline)

    return etree.ElementTree(root)

def write(file: Union[Path, str, BinaryIO], opml: Opml):
    et = serialize(opml)
    et.write(file, xml_declaration=True, encoding="UTF-8")
