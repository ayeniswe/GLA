import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import iterparse

from plugins.transformer.xml_transformer import XMLTransformer


def test_xml():
    xml = XMLTransformer()

    buffer = ""
    with open(
        os.path.join(os.path.dirname(__file__), "logs", "test.xml"), "r", encoding="utf-16-le"
    ) as f:
        line = f.readline()
        while line:
            buffer += line
            if line.strip("\n") == "</Event>":
                res = xml.transform(ET.fromstring(buffer))
                if res:
                    assert res.message != ""
                buffer = ""
            line = f.readline()
    buffer = ""

    for event, elem in iterparse(
        os.path.join(os.path.dirname(__file__), "logs", "test-jlu.log"),
        events=["end"],
    ):
        res = xml.transform(elem)
        if res:
            assert res.message != ""
