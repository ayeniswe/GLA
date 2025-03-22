from os import PathLike
from re import compile
from typing import Match, Optional

import dateparser
from typeguard import typechecked

from models.log import Log
from plugins.resolver.resolver import Resolver
from plugins.transformer.transformer import BaseTransformer
from utilities.strategy import RegexStrategy


@typechecked
class Log4jTransformer(BaseTransformer, Resolver):
    """
    The `Log4jTransformer` class is responsible for handling transformation
    of `log4j` log messages
    """

    def __init__(self, cache: bool = False):
        """Create a new `Log4jTransformer`

        NOTE: cache set to `True` will enable the use of the same strategy for
        future log entries seen by this instance
        """
        super().__init__(
            [
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{4}-\d{2}-\d{2})\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2}-\d{4}-\d{2})\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)\s+"
                        r"\[(?P<thread>[^\s]+)\]"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"-\s+(?P<msg>.+)"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<mod>[\w.]+)\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"-\s+(?P<msg>.+)\s+"
                        r"\[(?P<thread>[^\s]+)\]"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"\[(?P<thread>[^\s]+)\]"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"-\s+(?P<msg>.+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<mod>[\w.]+)\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"-\s+(?P<msg>.+)"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<mod>[\w.]+)\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"-\s+(?P<msg>.+)"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"\[(?P<thread>[^\s]+)\]"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"-\s+(?P<msg>.+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<msg>.+)\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"-\s+(?P<msg>.+)"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"-\s+(?P<msg>.+)"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"-\s+(?P<msg>.+)"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"-\s+(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"-\s+(?P<msg>.+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"-\s+(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"\[(?P<thread>[^\s]+)\]"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"-\s+(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"\[(?P<thread>[^\s]+)\]"
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"-\s+(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)"
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
                level=res.get("lvl"),
                module=res.get("mod"),
                source=res.get("thread"),
                timestamp=(dateparser.parse(res["time"])),
                message=res.get("msg"),
            )
        return None

    def _validate(self, path: PathLike) -> bool:
        with open(path, "r") as file:
            return self.resolve(file.readline().strip()) is not None
