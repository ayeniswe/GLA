from datetime import datetime
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
                    compile(
                        r"""(?P<host>[\w.:\]\[]+) (?:-|(?P<ident>[^\s-]+)) (?:-|(?P<user>[^\s-]+)) \[(?P<time>.+)\] "(?P<req>.+)" (?P<status>\d+) (?P<size>\d+) "(?:-|(?P<ref>.+))" "(?:-|(?P<agent>.+))" "(?:-|(?P<cook>.+))\""""
                    )
                ),
                # NCSA CLF
                RegexStrategy(
                    compile(
                        r"""(?P<host>[\w.:\]\[]+) (?:-|(?P<ident>[^\s-]+)) (?:-|(?P<user>[^\s-]+)) \[(?P<time>.+)\] "(?P<req>.+)" (?P<status>\d+) (?P<size>\d+)"""
                    )
                ),
                # CEF
                # RegexStrategy(
                #     compile(
                #         r"^CEF:(?P<cef>\d+)\|(?P<ven>.+?)\|(?P<prod>.+?)\|(?P<ver>.+?)\|(?P<sig>.+?)\|(?P<msg>.+?)\|(?P<lvl>.+?)\|(?<ext>.+)"
                #     )
                # ),
            ],
            cache,
        )

    def _transform(self, entry: str) -> Optional[Log]:
        match: Optional[Match[str]] = self.resolve(entry)
        if match:
            res = match.groupdict()

            # Building a custom message to better promote readability
            msg = f"Request: {res.get('req')} - Status: {res.get('status')} - Size: {res.get('size')}"
            ref = res.get("ref")
            if ref is not None:
                msg += f" - Referrer: {ref}"
            agent = res.get("agent")
            if agent is not None:
                msg += f" - User-Agent: {agent}"
            cookie = res.get("cook")
            if cookie is not None:
                msg += f" - Cookie: {cookie}"

            return Log(
                source=res.get("host"),
                timestamp=datetime.strptime(res.get('time'), "%d/%b/%Y:%H:%M:%S %z"),
                message=msg,
            )

    def _validate(self, path: PathLike) -> bool:
        with open(path, "r") as file:
            return self.resolve(file.readline().strip()) is not None
