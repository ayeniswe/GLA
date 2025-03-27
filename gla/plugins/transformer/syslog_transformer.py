"""
The `syslog_transformer` module is responsible for transforming `syslog` log
messages into structured `Log` objects based on the Syslog format standards.
It supports parsing both the older BFG RFC 3164 format and the more modern
IETF RFC 5424 format.
"""
import re
from typing import Match, Optional, Union

import dateparser

from gla.constants import LANGUAGES_SUPPORTED
from gla.models.log import Log
from gla.plugins.resolver.resolver import Resolver
from gla.plugins.transformer.transformer import BaseTransformerValidator
from gla.utilities.strategy import RegexStrategy


class SyslogTransformer(BaseTransformerValidator, Resolver):
    """
    The `SyslogTransformer` class is responsible for handling transformation
    of `syslog` log messages
    """

    def __init__(self, cache: bool = False):
        """Create a new `SyslogTransformer`

        NOTE: cache set to `True` will enable the use of the same strategy for
        future log entries seen by this instance
        """
        super().__init__(
            [
                # BFG RFC 3164 (older)
                RegexStrategy(
                    re.compile(
                        r"^<(?P<pri>\d{1,3})>"
                        r"(?P<time>[A-Z][a-z]{2}\s+\d{1,2} \d{2}:\d{2}:\d{2}) "
                        r"(?P<host>[^\s]+) "
                        r"(?P<proc>\w+)"
                        r"(?:\[(?P<pid>\d+)\])*:* "
                        r"(?P<msg>.+)"
                    )
                ),
                # IETF RFC 5424
                RegexStrategy(
                    re.compile(
                        r"^<(?P<pri>\d{1,3})>(?P<ver>\d{1,2}) "
                        r"(?P<time>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
                        r"(?:\.*\d{0,6}(?:Z|[-+]\d{2}:\d{2}))*) "
                        r"(?:(?P<host>[\w+.]+)|-) (?:(?P<proc>\w+)|-) "
                        r"(?:(?P<pid>\d+)|-) (?:(?P<msgid>\w+)|-) "
                        r"(?:\[(?P<struct>.+)\]|-)+ (?:BOM)*(?P<msg>.+)"
                    )
                ),
            ],
            cache,
        )

    def transform(self, entry: str) -> Optional[Log]:
        match: Optional[Match[str]] = self.resolve(entry)
        if match:
            res = match.groupdict()

            pri = res.get("pri")
            level = None
            if pri is not None:
                level = self._priority_to_lvl(pri)
            time = res.get("time")
            timedate = None
            if time is not None:
                timedate = dateparser.parse(time, languages=LANGUAGES_SUPPORTED)

            return Log(
                level=level,
                module=res.get("proc"),
                source=res.get("host"),
                timestamp=timedate,
                message=res.get("msg"),
            )
        return None

    def _priority_to_lvl(self, lvl: str) -> Union[str, None]:
        """Converts syslog priority levels to respective log severity levels"""
        res = int(lvl) % 8
        if res == 0:
            return "EMERGENCY"
        elif res == 1:
            return "ALERT"
        elif res == 2:
            return "CRITICAL"
        elif res == 3:
            return "ERROR"
        elif res == 4:
            return "WARN"
        elif res == 5:
            return "NOTICE"
        elif res == 6:
            return "INFO"
        elif res == 7:
            return "DEBUG"
        return None

    def validate(self, data: str) -> bool:
        if data == "sys":
            return True
        try:
            with open(data, "r", encoding="utf-8") as file:
                return self.resolve(file.readline().strip()) is not None
        except (FileNotFoundError, UnicodeDecodeError):
            return False
