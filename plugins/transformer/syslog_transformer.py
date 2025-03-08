from os import PathLike
from re import compile
from typing import Optional, Match
import dateparser
from typeguard import typechecked
from models.log import Log
from plugins.resolver.resolver import Resolver
from plugins.transformer.transformer import BaseTransformer
from utilities.strategy import RegexStrategy


@typechecked
class SyslogTransformer(BaseTransformer, Resolver):
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
                    compile(
                        r"^<(?P<pri>\d{1,3})>(?P<time>[A-Z][a-z]{2}\s+\d{1,2} \d{2}:\d{2}:\d{2}) (?P<host>[^\s]+) (?P<proc>\w+)(?:\[(?P<pid>\d+)\])*:* (?P<msg>.+)"
                    )
                ),
                # IETF RFC 5424
                RegexStrategy(
                    compile(
                        r"^<(?P<pri>\d{1,3})>(?P<ver>\d{1,2}) (?P<time>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.*\d{0,6}(?:Z|[-+]\d{2}:\d{2}))*) (?:(?P<host>[\w+.]+)|-) (?:(?P<proc>\w+)|-) (?:(?P<pid>\d+)|-) (?:(?P<msgid>\w+)|-) (?:\[(?P<struct>.+)\]|-)+ (?:BOM)*(?P<msg>.+)"
                    )
                ),
            ],
            cache,
        )

    def _transform(self, entry: str) -> Optional[Log]:
        match: Optional[Match[str]] = self.resolve(entry)
        if match:
            res = match.groupdict()
            return Log(
                level=self._priority_to_lvl(res.get("pri")),
                module=res.get("proc"),
                source=res.get("host"),
                timestamp=dateparser.parse(res.get("time")),
                message=res.get("msg"),
            )

    def _priority_to_lvl(self, lvl: str) -> str:
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

    def _validate(self, path: PathLike) -> bool:
        with open(path, "r") as file:
            return self.resolve(file.readline().strip()) is not None
