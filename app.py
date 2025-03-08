from xml.etree.ElementTree import Element, iterparse
from plugins.transformer.xml_transformer import XMLTransformer

x = XMLTransformer()
for event, elem in iterparse("test.log", events=["end"]):
    r = x._transform(elem)
    if r:
        print(r)
