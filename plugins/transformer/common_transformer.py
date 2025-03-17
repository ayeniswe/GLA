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
class CommonTransformer(BaseTransformer, Resolver):
    """
    The `CommonTransformer` class is responsible for handling transformation
    of common web servers `apache`, `sip`, and `ncsa` log messages
    """

    def __init__(self, cache: bool = False):
        """Create a new `CommonTransformer`

        NOTE: cache set to `True` will enable the use of the same strategy for
        future log entries seen by this instance
        """
        super().__init__(
            [
                # NCSA CLF
                RegexStrategy(
                    compile(
                        r"""(?P<host>[\w.:\]\[]+) (?:(?P<ident>[^\s-]+)|-) (?:(?P<user>[^\s-]+)|-) \[(?P<time>.+)\] "(?P<req>.+)" (?<status>\d+) (?P<size>\d+)"""
                    )
                ),
                # NCSA COMBINED CLF
                RegexStrategy(
                    compile(
                        r"""(?P<host>[\w.:\]\[]+) (?:(?P<ident>[^\s-]+)|-) (?:(?P<user>[^\s-]+)|-) \[(?P<time>.+)\] "(?P<req>.+)" (?<status>\d+) (?P<size>\d+) "(?:(?P<ref>.+)|-)" "(?:(?P<agent>.+)|-)" "(?:(?P<cook>.+)|-)"""
                    )
                ),
                # CEF
                RegexStrategy(
                    compile(
                        r"^CEF:(?P<cef>\d+)\|(?P<ven>.+?)\|(?P<prod>.+?)\|(?P<ver>.+?)\|(?P<sig>.+?)\|(?P<msg>.+?)\|(?P<lvl>.+?)\|(?<ext>.+)"
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
                module=res.get("proc"),
                source=res.get("host",res.get("src")),
                timestamp=dateparser.parse(res.get("time")),
                message=res.get("msg"),
            )


    def _validate(self, path: PathLike) -> bool:
        with open(path, "r") as file:
            return self.resolve(file.readline().strip()) is not None
