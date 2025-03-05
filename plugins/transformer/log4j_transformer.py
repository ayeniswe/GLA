from re import compile
from typing import Pattern, Match
import dateparser
from typing import List, Union
from log import Log
from plugins.transformer.transformer import Transformer


# Supports the division between two attributes in log message
# rather that division exists or doesn't
DIVIDER_RE = r"[^\s]*"
# Supports the gathering timestamps in log messages
TIME_RE = r"(?P<time>(?:\d{2,4}-\d{2,4}-\d{2,4})*[T\s]*(\d{2}:\d{2}:\d{2}(?:.\d{3})*)*)"
# Supports the gathering of common levels in log messages
LEVEL_RE = r"[^a-zA-Z\s]*(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)[^a-zA-Z\s]*"
# Support the gathering of abritrary log messages
MSG_RE = r"(?P<msg>.+)"
# Supports the gathering of any inner casing for the module or source in log message
# and allows $, -, . characters to be used in that module or source
SOURCE_RE = r"[^a-zA-Z\s]*(?P<src>[\w$.]+)[^a-zA-Z\s]*"
MODULE_RE = r"[^a-zA-Z\s]*(?P<mod>[\w$.]+)[^a-zA-Z\s]*"


class Log4jTransformer(Transformer):
    """
    The `Log4jTransformer` class is responsible for handling transformation
    of `log4j` log messages
    """

    def __init__(self, strategies: List[str]):
        """Create a new `Log4jTransformer`

        Args:
            regex (list(str)): A list of regex strings to resolve a `log4j` log format
        """
        self._strategies: List[Pattern] = []
        for regex in strategies:
            self._strategies.append(compile(regex))

    def transform(self, line: str) -> Union[Log, None]:
        match = self._resolve(line)
        if match:
            match = match.groupdict()
            return Log(
                level=match.get("lvl"),
                module=match.get("mod"),
                source=match.get("thread"),
                timestamp=(
                    dateparser.parse(match["time"]) if match.get("time") else None
                ),
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
