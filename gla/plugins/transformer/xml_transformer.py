"""
The `xml_transformer` module is responsible for transforming XML-based log
messages into structured `Log` objects. It supports various XML formats,
including `Java Logging Util` (JLU)
"""
from typing import Any, Dict, Optional
from xml.etree.ElementTree import Element

import dateparser

from gla.constants import LANGUAGES_SUPPORTED
from gla.models.log import Log
from gla.plugins.resolver.resolver import Resolver
from gla.plugins.transformer.transformer import BaseTransformerValidator
from gla.utilities.strategy import Strategy

class BaseXMLTransformer(BaseTransformerValidator):

    def transform(self, entry: Element) -> Optional[Log]:
        mapping: Optional[dict] = self.resolve(entry)
        if mapping:
            time = mapping.get("timestamp")
            timedate = None
            if time is not None:
                timedate = dateparser.parse(time, languages=LANGUAGES_SUPPORTED)
            return Log(
                level=mapping.get("level"),
                module=mapping.get("module"),
                source=mapping.get("source"),
                timestamp=timedate,
                message=mapping.get("message"),
            )
        return None


class JLU(Strategy):
    """
    The `JLU` class is responsible for handling transformations
    of `Java Logging Util` xml DTD schema
    """

    def match(self, entry: Element) -> Optional[dict]:
        if entry.tag == "record":
            res = {}
            for child in entry.getiterator():
                if child.tag == "level":
                    res["level"] = child.text
                if child.tag == "message":
                    res["message"] = child.text
                if child.tag == "logger":
                    res["module"] = child.text
                if child.tag == "thread":
                    res["source"] = child.text
                if child.tag == "date":
                    res["timestamp"] = child.text
            return res
        return None


class XMLTransformer(BaseXMLTransformer, Resolver):
    """
    The `XMLTransformer` class is responsible for handling transformation
    of `xml` log messages
    """

    def __init__(self, cache: bool = False):
        """Create a new `XMLTransformer`

        NOTE: cache set to `True` will enable the use of the same strategy for
        future log entries seen by this instance
        """
        super().__init__(
            [JLU()],
            cache,
        )

    def validate(self, data: Dict[str, Any]) -> bool:
        if data["data"] == "xml":
            return True
        return False
