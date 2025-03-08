from os import PathLike
from typing import Optional
import dateparser
from xml.etree.ElementTree import Element
from typeguard import typechecked
from models.log import Log
from plugins.resolver.resolver import Resolver
from plugins.transformer.transformer import BaseTransformer
from utilities.strategy import Strategy
from magic.magic import from_file


@typechecked
class JLUReader(Strategy):
    """
    The `JLUReader` class is responsible for handling transformations
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


@typechecked
class WinEventsReader(Strategy):
    """
    The `WinEventsReader` class is responsible for handling transformations
    of `Windows Events` from `.evtx` logs
    """

    def match(self, entry: Element) -> Optional[dict]:
        pass  # TODO


@typechecked
class XMLTransformer(BaseTransformer, Resolver):
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
            [JLUReader(), WinEventsReader()],
            cache,
        )

    def _transform(self, entry: Element) -> Optional[Log]:
        mapping: Optional[dict] = self.resolve(entry)
        if mapping:
            return Log(
                level=mapping["level"],
                module=mapping["module"],
                source=mapping["source"],
                timestamp=dateparser.parse(mapping["timestamp"]),
                message=mapping["message"],
            )

    def _validate(self, path: PathLike) -> bool:
        return from_file(path, True) == "text/xml"
