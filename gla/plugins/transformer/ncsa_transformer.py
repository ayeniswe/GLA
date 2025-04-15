"""
The `ncsa_transformer` module is responsible for transforming common web server
NCSA log entries into structured `Log` objects. It supports both the NCSA Combined
Log Format (CLF) and the standard NCSA CLF
"""
import re
from datetime import datetime
from typing import Any, Dict, Match, Optional

from gla.analyzer.iterator import UnstructuredBaseResolverBreakerMixIn
from gla.models.log import Log
from gla.plugins.resolver.resolver import Resolver
from gla.plugins.transformer.transformer import (BaseTransformerValidator,
                                                 RegexBreakerStrategy)


class NcsaTransformer(BaseTransformerValidator, Resolver, UnstructuredBaseResolverBreakerMixIn):
    """
    The `NcsaTransformer` class is responsible for handling transformation
    of common web servers `ncsa` log messages
    """

    def __init__(self):
        """Create a new `NcsaTransformer`
        """
        super().__init__(
            [
                # NCSA COMBINED CLF
                RegexBreakerStrategy(
                    re.compile(
                        r"(?P<host>[\w.:\]\[]+) "
                        r"(?:-|(?P<ident>[^\s-]+)) "
                        r"(?:-|(?P<user>[^\s-]+)) "
                        r"\[(?P<time>.+)\] "
                        r'"(?P<req>.+)" '
                        r"(?P<status>\d+) "
                        r"(?P<size>\d+) "
                        r'"(?:-|(?P<ref>.+))" '
                        r'"(?:-|(?P<agent>.+))" '
                        r'"(?:-|(?P<cook>.+))"'
                    )
                ),
                # NCSA CLF
                RegexBreakerStrategy(
                    re.compile(
                        r"(?P<host>[\w.:\]\[]+) "
                        r"(?:-|(?P<ident>[^\s-]+)) "
                        r"(?:-|(?P<user>[^\s-]+)) "
                        r"\[(?P<time>.+)\] "
                        r'"(?P<req>.+)" '
                        r"(?P<status>\d+) "
                        r"(?P<size>\d+)"
                    )
                ),
            ],
            False
        )

    def transform(self, entry: str) -> Optional[Log]:
        match: Optional[Match[str]] = self._cache_strategy.do_action(entry)
        if match:
            res = match.groupdict()

            # Building a custom message to better promote readability
            msg = (
                f"Request: {res.get('req')} - Status: {res.get('status')} - Size: {res.get('size')}"
            )
            ref = res.get("ref")
            if ref is not None:
                msg += f" - Referrer: {ref}"
            agent = res.get("agent")
            if agent is not None:
                msg += f" - User-Agent: {agent}"
            cookie = res.get("cook")
            if cookie is not None:
                msg += f" - Cookie: {cookie}"

            time = res.get("time")
            timedate = None
            if time is not None:
                timedate = datetime.strptime(time, "%d/%b/%Y:%H:%M:%S %z")
            return Log(
                source=res.get("host"),
                timestamp=timedate,
                message=msg,
            )
        return None

    def validate(self, data: Dict[str, Any]) -> bool:
        try:
            return self.resolve((data["data"], data["encoding"])) is not None
        except (FileNotFoundError, UnicodeDecodeError):
            return False
