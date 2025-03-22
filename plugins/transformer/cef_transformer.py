from datetime import datetime
from os import PathLike
from re import compile
from typing import Match, Optional

from typeguard import typechecked

from models.log import Log
from plugins.resolver.resolver import Resolver
from plugins.transformer.transformer import BaseTransformer
from utilities.strategy import RegexStrategy


@typechecked
class CefTransformer(BaseTransformer, Resolver):
    """
    The `CefTransformer` class is responsible for handling transformation
    of common event  log messages
    """

    def __init__(self, cache: bool = False):
        """Create a new `CefTransformer`

        NOTE: cache set to `True` will enable the use of the same strategy for
        future log entries seen by this instance
        """
        super().__init__(
            [
                # CEF
                RegexStrategy(
                    compile(
                        r"^CEF:(?P<cef>\d+)\|"
                        r"(?P<ven>.+?)\|"
                        r"(?P<prod>.+?)\|"
                        r"(?P<ver>.+?)\|"
                        r"(?P<sig>.+?)\|"
                        r"(?P<msg>.+?)\|"
                        r"(?P<lvl>.+?)\|"
                        r"(?P<ext>.+)"
                    )
                ),
            ],
            cache,
        )

    def _transform(self, entry: str) -> Optional[Log]:

        match: Optional[Match[str]] = self.resolve(entry)

        if match:
            res = match.groupdict()

            # Structuring message from CEF fields
            msg = (
                f"CEF Version: {res.get('cef')} - Vendor: {res.get('ven')} - "
                f"Product: {res.get('prod')} - Version: {res.get('ver')} - "
                f"Signature: {res.get('sig')} - Severity: {res.get('lvl')}"
            )
            ext = res.get("ext")
            if ext:
                msg += f" - Extensions: {ext}"

            time = res.get("time")
            timedate = None
            if time is not None:
                timedate = datetime.strptime(time, "%d/%b/%Y:%H:%M:%S %z")
        return Log(
            source=res.get("host"),
            timestamp=timedate,
            message=msg,
        )

    def _validate(self, path: PathLike) -> bool:
        with open(path, "r") as file:
            return self.resolve(file.readline().strip()) is not None
