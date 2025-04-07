"""
The `xmlfragment_transformer` module is responsible for transforming fragmented XML-based log
messages into structured `Log` objects. It supports various XML formats,
including `Windows Event Logs`
"""
from typing import Any, Dict, Optional, Union
from xml.etree.ElementTree import Element

from gla.analyzer.iterator import UnstructuredResolverBreakerMixIn
from gla.plugins.resolver.resolver import Resolver
from lxml.etree import XMLSyntaxError
from gla.plugins.transformer.transformer import Breaker
from gla.plugins.transformer.xml_transformer import BaseXMLTransformer
from gla.utilities.strategy import Strategy
from gla.typings.alias import FileDescriptorOrPath
from lxml.etree import iterparse

class WinEvent(Strategy, Breaker):
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
    
    @property
    def breaker(self) -> str:
        return "</Event>"


class XMLFragmentTransformer(BaseXMLTransformer, UnstructuredResolverBreakerMixIn):
    """
    The `XMLFragmentTransformer` class is responsible for handling transformation
    of fragmented `xml` log messages
    """

    def __init__(self, cache: bool = False):
        """Create a new `XMLFragmentTransformer`

        NOTE: cache set to `True` will enable the use of the same strategy for
        future log entries seen by this instance
        """
        super().__init__(
            [WinEvent()],
            cache,
        )

    def validate(self, data: Dict[str, Any]) -> bool:
        if data["data"] == "xml-frag":
            return True
        try:
            path: FileDescriptorOrPath = data["data"]
            # We need to keep trying until a error occurs which should happen
            # pretty early more than not
            for _ in iterparse(path):
                ...
        except XMLSyntaxError:
            return True