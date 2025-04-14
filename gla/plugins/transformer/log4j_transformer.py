"""
The 'log4j_transformer' module contains the `Log4jTransformer` class,
which is tasked with converting Log4j log messages into structured `Log` objects.
"""

import re
from typing import Any, Dict, Match, Optional

import dateparser

from gla.analyzer.iterator import Breaker, UnstructuredBaseResolverBreakerMixIn
from gla.constants import LANGUAGES_SUPPORTED
from gla.models.log import Log
from gla.plugins.resolver.resolver import Resolver
from gla.plugins.transformer.transformer import BaseTransformerValidator, RegexBreakerStrategy


class Log4jTransformer(BaseTransformerValidator, Resolver, UnstructuredBaseResolverBreakerMixIn):
    """
    The `Log4jTransformer` class is responsible for handling transformation
    of `log4j` log messages
    """

    def __init__(self):
        """Create a new `Log4jTransformer`
        """
        super().__init__(
            [
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<time>\d{4}-\d{2}-\d{2})\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<time>\d{2}-\d{4}-\d{2})\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)\s+"
                        r"\[(?P<thread>[^\s]+)\]"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"-\s+(?P<msg>.+)"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<mod>[\w.]+)\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"-\s+(?P<msg>.+)\s+"
                        r"\[(?P<thread>[^\s]+)\]"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"\[(?P<thread>[^\s]+)\]"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"-\s+(?P<msg>.+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<mod>[\w.]+)\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"-\s+(?P<msg>.+)"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<mod>[\w.]+)\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"-\s+(?P<msg>.+)"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<mod>[\w.]+)\s+-\s+"
                        r"(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"\[(?P<thread>[^\s]+)\]"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"-\s+(?P<msg>.+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<msg>.+)\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"-\s+(?P<msg>.+)"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"-\s+(?P<msg>.+)"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"-\s+(?P<msg>.+)"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"-\s+(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"-\s+(?P<msg>.+)\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"-\s+(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"\[(?P<thread>[^\s]+)\]"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"-\s+(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+"
                        r"\[(?P<thread>[^\s]+)\]"
                    )
                ),
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<mod>[\w.]+)\s+"
                        r"-\s+(?P<msg>.+)\s+"
                        r"(?P<time>\d{2,4}-\d{2,4}-\d{2,4})\s+"
                        r"(?:\[(?P<thread>[^\s]+)\]\s+)*"
                        r"(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)"
                    )
                ),
            ],
            False
        )

    def transform(self, entry: str) -> Optional[Log]:
        match: Optional[Match[str]] = self.resolve(entry)
        if match:
            res = match.groupdict()
            return Log(
                level=res.get("lvl"),
                module=res.get("mod"),
                source=res.get("thread"),
                timestamp=(dateparser.parse(res["time"], languages=LANGUAGES_SUPPORTED)),
                message=res.get("msg"),
            )
        return None

    def validate(self, data: Dict[str, Any]) -> bool:
        try:
            return self.resolve((data["data"], data["encoding"])) is not None
        except (FileNotFoundError, UnicodeDecodeError):
            return False
