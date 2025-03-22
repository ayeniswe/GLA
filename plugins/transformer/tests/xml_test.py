import os
from xml.etree.ElementTree import iterparse

from plugins.transformer.xml_transformer import XMLTransformer


def test_xml():
    xml = XMLTransformer()

    for event, elem in iterparse(
        os.path.join(os.path.dirname(__file__), "logs", "test.xml"),
        events=["end"],
    ):
        res = xml._transform(elem)
        if res:
            assert res.message != ""

    for event, elem in iterparse(
        os.path.join(os.path.dirname(__file__), "logs", "test-jlu.log"),
        events=["end"],
    ):
        res = xml._transform(elem)
        if res:
            assert res.message != ""
