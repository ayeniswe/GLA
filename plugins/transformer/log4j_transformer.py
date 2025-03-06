from re import compile
from typing import Pattern, Match
import dateparser
from typing import List, Union
from log import Log
from plugins.transformer.transformer import Transformer


class Log4jTransformer(Transformer):
    """
    The `Log4jTransformer` class is responsible for handling transformation
    of `log4j` log messages
    """

    def __init__(self):
        """Create a new `Log4jTransformer`"""
        self._strategies: List[Pattern] = [
            # Standard log4j format but different orders
            compile(
                r"^(?P<time>\d{4}-\d{2}-\d{2})\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
            ),
            compile(
                r"^(?P<time>\d{2}-\d{4}-\d{2})\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
            ),
            compile(
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
            ),
            compile(
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>\w+)\]\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
            ),
            compile(
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]",
            ),
            compile(
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+\[(?P<thread>\w+)\]\s+-\s+(?P<msg>.+)",
            ),
            compile(
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]",
            ),
            compile(
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>\w+)\]",
            ),
            compile(
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
            ),
            compile(
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
            ),
            compile(
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
            ),
            compile(
                r"^\[(?P<thread>\w+)\]\s+(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
            ),
            compile(
                r"^\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
            ),
            compile(
                r"^\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})",
            ),
            compile(
                r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>\w+)\]\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})",
            ),
            compile(
                r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+\[(?P<thread>\w+)\]\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})",
            ),
            compile(
                r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<time>\d{2}-\d{2}-\d{4})",
            ),
            compile(
                r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]",
            ),
            compile(
                r"^(?P<mod>[\w.]+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
            ),
            compile(
                r"^(?P<mod>[\w.]+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]\s+(?P<msg>.+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
            ),
            compile(
                r"^(?P<mod>[\w.]+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+-\s+(?P<msg>.+)",
            ),
            compile(
                r"^(?P<mod>[\w.]+)\s+\[(?P<thread>\w+)\]\s+(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+-\s+(?P<msg>.+)",
            ),
            compile(
                r"^(?P<mod>[\w.]+)\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+-\s+(?P<msg>.+)",
            ),
            compile(
                r"^(?P<mod>[\w.]+)\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})",
            ),
            compile(
                r"^(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>\w+)\]\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})",
            ),
            compile(
                r"^(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<time>\d{2}-\d{2}-\d{4})",
            ),
            compile(
                r"^(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]",
            ),
            compile(
                r"^(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>\w+)\]",
            ),
            compile(
                r"^(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
            ),
        ]

    def transform(self, line: str) -> Union[Log, None]:
        match = self._resolve(line)
        if match:
            match = match.groupdict()
            return Log(
                level=match.get("lvl"),
                module=match.get("mod"),
                source=match.get("thread"),
                timestamp=(dateparser.parse(match["time"])),
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
