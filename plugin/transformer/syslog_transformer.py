from re import compile
from typing import Pattern, Match
import dateparser
from typing import List, Union
from model.log import Log
from plugin.transformer.transformer import Transformer


class SyslogTransformer(Transformer):
    """
    The `SyslogTransformer` class is responsible for handling transformation
    of `syslog` log messages
    """

    def __init__(self):
        """Create a new `SyslogTransformer`"""
        self._strategies: List[Pattern] = [
            # BFG RFC 3164 (older)
            compile(
                r"^<(?P<pri>\d{1,3})>(?P<time>[A-Z][a-z]{2}\s+\d{1,2} \d{2}:\d{2}:\d{2}) (?P<host>[\w+.]+) (?P<proc>\w+)(?:\[(?P<pid>\d+)\])*:* (?P<msg>.+)"
            ),
            # IETF RFC 5424
            compile(
                r"^<(?P<pri>\d{1,3})>(?P<ver>\d{1,2}) (?P<time>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:.\d{1,6}(?:Z|[-+]\d{2}:\d{2}))*) (?:(?P<host>[\w+.]+)|-) (?:(?P<proc>\w+)|-) (?:(?P<pid>\d+)|-) (?:(?P<msgid>\w+)|-) (?:\[(?P<struct>.+)\]|-)+ (?:BOM)*(?P<msg>.+)"
            ),
        ]

    def transform(self, line: str) -> Union[Log, None]:
        match = self._resolve(line)
        if match:
            match = match.groupdict()
            return Log(
                level=self._priority_to_lvl(match.get("pri")),
                module=match.get("proc"),
                source=match.get("host"),
                timestamp=dateparser.parse(match.get("time")),
                message=match.get("msg"),
            )
        else:
            return None

    def _resolve(self, line: str) -> Union[Match[str], None]:
        """Resolves to the correct formatter to parse the log

        Returns:
            Match: A `Match` object or `None` if the format can not be determined
        """
        for strategy in self._strategies:
            match = strategy.match(line)
            if match:
                return match
        return None

    def _priority_to_lvl(self, lvl: str) -> str:
        """Converts syslog priority levels to respective GLA log levels"""
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
