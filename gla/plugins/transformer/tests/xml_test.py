import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import iterparse

from gla.plugins.transformer.xml_transformer import XMLTransformer
from gla.plugins.transformer.xmlfragment_transformer import XMLFragmentTransformer


def test_xml():
    xmlfrag = XMLFragmentTransformer()

    buffer = ""
    with open(
        os.path.join(os.path.dirname(__file__), "logs", "test.xml"), "r", encoding="utf-16-le"
    ) as f:
        line = f.readline()
        while line:
            buffer += line
            if line.strip("\n") == "</Event>":
                res = xmlfrag.transform(ET.fromstring(buffer))
                if res:
                    assert res.message != ""
                buffer = ""
            line = f.readline()
    buffer = ""

    xml = XMLTransformer()
    
    for event, elem in iterparse(os.path.join(os.path.dirname(__file__), "logs", "test-jlu.log")):

        res = xml.transform(elem)
        if res:
            assert res.message != ""
