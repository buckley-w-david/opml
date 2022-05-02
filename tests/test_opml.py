from datetime import datetime
import io

from opml import __version__
from opml.models import Opml, Head, Body, Version, Outline
from opml import writer
from opml import reader

def test_writer():
    opml = Opml(
        version=Version.VERSION2,
        head=Head(
            title="test",
        ),
        body=Body(
            outlines=[
                Outline(
                    text="NYT baseball",
                    attributes={
                        "xmlUrl": "http://rss.nytimes.com/services/xml/rss/nyt/Baseball.xml",
                        "name": "newFeed",
                        "created": datetime(2015, 9, 7, 20, 53, 13),
                        "type": "rss"
                    },
                )
            ]
        )
    )
    output = io.BytesIO()
    writer.write(output, opml)
    output.seek(0)

    assert output.read() == b'<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<opml version="2.0"><head><title>test</title></head><body><outline text="NYT baseball" xmlUrl="http://rss.nytimes.com/services/xml/rss/nyt/Baseball.xml" name="newFeed" created="Mon, 07 Sep 2015 20:53:13 -0000" type="rss"/></body></opml>'

def test_reader_version():
    result = reader.read('tests/writer.opml')
    assert result.version == Version.VERSION2

def test_reader_header():
    result = reader.read('tests/writer.opml')
    assert result.head.title == 'opml Test Suite'
    assert result.head.date_modified == datetime(2006, 7, 17, 0, 0, 0)
    assert result.head.owner_name == "David Buckley"

def test_reader_body():
    result = reader.read('tests/writer.opml')
    assert len(result.body.outlines) == 1
    assert result.body.outlines[0].text == "Headers"
    next_level = result.body.outlines[0].sub_outlines[0]
    assert next_level.text == "Level 2"
    next_level = next_level.sub_outlines[0]
    assert next_level.text == "Level 3"
    next_level = next_level.sub_outlines[0]
    assert next_level.text == "Level 4"
    next_level = next_level.sub_outlines[0]
    assert next_level.text == "Level 5"
