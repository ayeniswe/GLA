"""
The `xml_transformer` module is responsible for transforming XML-based log
messages into structured `Log` objects. It supports various XML formats,
including `Java Logging Util` (JLU)
"""
from typing import Any, Dict, Optional, Tuple
from xml.etree.ElementTree import Element

import dateparser

from gla.analyzer.iterator import Mode, Structured, StructuredMixIn
from gla.constants import LANGUAGES_SUPPORTED
from gla.models.log import Log
from gla.plugins.resolver.resolver import BaseResolver, Resolver
from gla.plugins.transformer.transformer import BaseTransformer, BaseTransformerValidator
from gla.utilities.strategy import Strategy, StrategyAction
from lxml.etree import iterparse, XMLSyntaxError
from gla.typings.alias import FileDescriptorOrPath

class BaseXMLTransformer(BaseTransformerValidator, Resolver):

    def isfrag(path: FileDescriptorOrPath, encoding: str) -> bool:
        """
        Heuristically determines if the given XML file is a fragment.

        Parses the file incrementally and treats it as a fragment if a parsing 
        error occurs early (i.e., shallow depth).

        Args:
            path (FileDescriptorOrPath): The path or file-like object pointing to the XML content.
            encoding (str): The encoding of the file.

        Returns:
            bool: True if the file is likely an XML fragment, False if it's a full document.
        """
        try:
            # We need to keep trying until a error occurs which should happen
            # pretty early more than not
            for depth, _ in enumerate(iterparse(path, encoding=encoding, events=["start"])):
                if depth > 50:
                    return False
            return False
        except XMLSyntaxError:
            return True

    def transform(self, entry: Element) -> Optional[Log]:
        mapping: Optional[dict] = self._cache_strategy.do_action(entry)
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


class JLU(StrategyAction):
    """
    The `JLU` class is responsible for handling transformations
    of `Java Logging Util` xml DTD schema
    """

    def match(self, entry: Tuple[FileDescriptorOrPath, str]) -> Optional[dict]:
        for depth, elem in enumerate(Structured(entry[0], entry[1], Mode.XML)):
            # Check may run too deep
            if depth > 12:
                return False
            
            if elem.tag == "record":
                # Core tags that are typically always present in JUL logs
                required_tags = {"date", "logger", "level", "message"}
                child_tags = {child.tag for child in elem}
                # Check if the required subset exists
                if required_tags.issubset(child_tags):
                    return True

    def do_action(self, entry: Element) -> Optional[dict]:
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


class XMLTransformer(BaseXMLTransformer, Resolver, StructuredMixIn):
    """
    The `XMLTransformer` class is responsible for handling transformation
    of `xml` log messages
    """

    @property
    def mode(self) -> str:
        return Mode.XML
    
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
        path: FileDescriptorOrPath = data["data"]
        encoding = data["encoding"]
        if not BaseXMLTransformer.isfrag(path, encoding):
            self.resolve((path, encoding))
            return True
