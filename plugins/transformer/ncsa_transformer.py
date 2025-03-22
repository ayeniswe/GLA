"""
The `ncsa_transformer` module is responsible for transforming common web server
NCSA log entries into structured `Log` objects. It supports both the NCSA Combined
Log Format (CLF) and the standard NCSA CLF
"""
import re
from datetime import datetime
from os import PathLike
from typing import Match, Optional

from typeguard import typechecked

from models.log import Log
from plugins.resolver.resolver import Resolver
from plugins.transformer.transformer import BaseTransformer
from utilities.strategy import RegexStrategy


@typechecked
class NcsaTransformer(BaseTransformer, Resolver):
    """
    The `NcsaTransformer` class is responsible for handling transformation
    of common web servers `ncsa` log messages
    """

    def __init__(self, cache: bool = False):
        """Create a new `NcsaTransformer`

        NOTE: cache set to `True` will enable the use of the same strategy for
        future log entries seen by this instance
        """
        super().__init__(
            [
                # NCSA COMBINED CLF
                RegexStrategy(
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
                RegexStrategy(
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
            cache,
        )

    def _transform(self, entry: str) -> Optional[Log]:
        match: Optional[Match[str]] = self.resolve(entry)
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

    def validate(self, path: PathLike) -> bool:
        with open(path, "r", encoding="utf-8") as file:
            return self.resolve(file.readline().strip()) is not None
