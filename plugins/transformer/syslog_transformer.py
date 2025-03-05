from re import compile
from typing import Pattern, Match
import dateparser
from typing import List, Union
from log import Log
from plugins.transformer.transformer import Transformer


class SyslogTransformer(Transformer):
    """
    The `SyslogTransformer` class is responsible for handling transformation
    of `syslog` log messages
    """

    def __init__(self, strategies: List[str]):
        """Create a new `SyslogTransformer`

        Args:
            regex (list(str)): A list of regex strings to resolve a `syslog` log format
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
