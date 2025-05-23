"""
The `xml_transformer` module is responsible for transforming XML-based log
messages into structured `Log` objects. It supports various XML formats,
including `Java Logging Util` (JLU) and `Windows Event Logs`
"""
from typing import Optional, Union
from xml.etree.ElementTree import Element

import dateparser

from gla.constants import LANGUAGES_SUPPORTED
from gla.models.log import Log
from gla.plugins.resolver.resolver import Resolver
from gla.plugins.transformer.transformer import BaseTransformerValidator
from gla.utilities.strategy import Strategy


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


class WinEvent(Strategy):
    """
    The `WinEvent` class is responsible for handling transformations
    of `Windows Events` from `.evtx` logs
    """

    NS = "{http://schemas.microsoft.com/win/2004/08/events/event}"

    def match(self, entry: Element) -> Optional[dict]:
        if entry.tag != f"{self.NS}Event":
            return None

        res = {
            "module": self._get_attribute(entry, f"{self.NS}System/{self.NS}Provider", "Name"),
            "level": self._to_lvl(self._get_text(entry, f"{self.NS}System/{self.NS}Level")),
            "source": self._get_text(entry, f"{self.NS}System/{self.NS}Computer"),
            "timestamp": self._get_attribute(
                entry, f"{self.NS}System/{self.NS}TimeCreated", "SystemTime"
            ),
        }

        event_id = self._get_text(entry, f"{self.NS}System/{self.NS}EventID")
        data_entries = entry.findall(f".//{self.NS}EventData/{self.NS}Data")

        extra_data = {data.get("Name"): data.text for data in data_entries if data.get("Name")}
        data_pieces = [data.text for data in data_entries if not data.get("Name") and data.text]

        message_parts = [f"EventID: {event_id}"]
        if extra_data:
            message_parts.append(str(extra_data))
        if data_pieces:
            message_parts.append(" ".join(data_pieces))

        res["message"] = " - ".join(message_parts)
        return res

    def _to_lvl(self, level: Union[str, None]):
        """Converts window events integer levels to respective log severity levels"""
        if level == "1":
            return "CRITICAL"
        if level == "2":
            return "ERROR"
        if level == "3":
            return "WARNING"
        if level == "4":
            return "INFO"
        if level == "5":
            return "DEBUG"
        else:
            return None

    def _get_text(self, entry: Element, path: str) -> Optional[str]:
        element = entry.find(f".//{path}")
        return element.text if element is not None else None

    def _get_attribute(self, entry: Element, path: str, attr: str) -> Optional[str]:
        element = entry.find(f"./{path}")
        return element.get(attr) if element is not None else None


class XMLTransformer(BaseTransformerValidator, Resolver):
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
            [JLU(), WinEvent()],
            cache,
        )

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

    def validate(self, data: str) -> bool:
        if data == "xml":
            return True
        return False
