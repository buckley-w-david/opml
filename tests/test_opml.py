from datetime import datetime
import io
from pathlib import Path

from opml import __version__
from opml.models import Opml, Head, Body, Version, Outline
from opml import writer


def test_version():
    assert __version__ == '0.1.0'

def test_writer():
    opml = Opml(
        version=Version.VERSION2,
        head=Head(),
        body=Body(
            outlines=[
                Outline(
                    attributes={
                        "text": "NYT baseball",
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

    assert output.read() == b'<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<opml version="2.0"><head/><body><outline text="NYT baseball" xmlUrl="http://rss.nytimes.com/services/xml/rss/nyt/Baseball.xml" name="newFeed" created="Mon, 07 Sep 2015 20:53:13 -0000" type="rss"/></body></opml>'
