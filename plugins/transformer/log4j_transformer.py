from os import PathLike
from re import compile
import dateparser
from typing import Optional, Match
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
                # Standard log4j format but different orders
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{4}-\d{2}-\d{2})\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2}-\d{4}-\d{2})\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)\s+\[(?P<thread>[^\s]+)\]",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+(?:\[(?P<thread>[^\s]+)\]\s+)*-\s+(?P<msg>.+)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+-\s+(?P<msg>.+)\s+\[(?P<thread>[^\s]+)\]",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>[^\s]+)\]",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+-\s+(?P<msg>.+)\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+-\s+(?P<msg>.+)\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)\s+(?P<time>\d{2,4}-\d{2,4}-\d{2,4})",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+-\s+(?P<msg>.+)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+-\s+(?P<msg>.+)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)\s+(?P<time>\d{2,4}-\d{2,4}-\d{2,4})",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<msg>.+)\s+(?P<time>\d{2,4}-\d{2,4}-\d{2,4})",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<time>\d{2,4}-\d{2,4}-\d{2,4})",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)\s+(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+\[(?P<thread>[^\s]+)\]",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+-\s+(?P<msg>.+)\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<msg>.+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+-\s+(?P<msg>.+)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+-\s+(?P<msg>.+)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+-\s+(?P<msg>.+)",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+-\s+(?P<msg>.+)\s+(?P<time>\d{2,4}-\d{2,4}-\d{2,4})",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<msg>.+)\s+(?P<time>\d{2,4}-\d{2,4}-\d{2,4})",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+-\s+(?P<msg>.+)\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<time>\d{2,4}-\d{2,4}-\d{2,4})",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+-\s+(?P<msg>.+)\s+(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+\[(?P<thread>[^\s]+)\]",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)\s+(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>[^\s]+)\]",
                    )
                ),
                RegexStrategy(
                    compile(
                        r"^(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)\s+(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+(?:\[(?P<thread>[^\s]+)\]\s+)*(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
                    )
                ),
            ],
            cache,
        )

    def _transform(self, line: str) -> Optional[Log]:
        match: Optional[Match[str]] = self.resolve(line)
        if match:
            res = match.groupdict()
            return Log(
                level=res.get("lvl"),
                module=res.get("mod"),
                source=res.get("thread"),
                timestamp=(dateparser.parse(res["time"])),
                message=res.get("msg"),
            )
        else:
            return None

    def _validate(self, path: PathLike) -> bool:
        with open(path, "r") as file:
            return self.resolve(file.readline().strip()) is not None
