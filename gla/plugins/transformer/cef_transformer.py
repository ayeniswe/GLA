"""
The 'cef_transformer' module defines the `CefTransformer` class,
which is responsible for transforming common event log (CEF) messages into structured
`Log` objects.
"""
import re
from typing import Match, Optional, Union

from models.log import Log
from plugins.resolver.resolver import Resolver
from plugins.transformer.transformer import BaseTransformer
from typeguard import typechecked
from utilities.strategy import RegexStrategy


@typechecked
class CefTransformer(BaseTransformer, Resolver):
    """
    The `CefTransformer` class is responsible for handling transformation
    of common event  log messages
    """

    def _to_lvl(self, lvl: int) -> Union[str, None]:
        """Converts event integer severity levels to respective severity levels"""
        if lvl > 0 and lvl <= 3:
            return "LOW"
        elif lvl > 3 and lvl <= 6:
            return "MEDIUM"
        elif lvl > 7 and lvl <= 8:
            return "HIGH"
        elif lvl > 8:
            return "VERY HIGH"
        return None

    def __init__(self, cache: bool = False):
        """Create a new `CefTransformer`

        NOTE: cache set to `True` will enable the use of the same strategy for
        future log entries seen by this instance
        """
        super().__init__(
            [
                # CEF
                RegexStrategy(
                    re.compile(
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

    def transform(self, entry: str) -> Optional[Log]:

        match: Optional[Match[str]] = self.resolve(entry)

        if match:
            res = match.groupdict()

            # Some messages may have more metadata than others
            msg = res.get("msg", "")
            ext = res.get("ext")
            if ext:
                msg += f" - Extensions: {ext}"

            lvl = res.get("lvl")
            lvl_str = None
            if lvl is not None:
                lvl_str = self._to_lvl(int(lvl))

        return Log(
            source=f"{res.get('ven')} {res.get('prod')} {res.get('ver')}",
            module=f"Signature ID: {res.get('sig')}",
            level=lvl_str,
            message=msg,
        )

    def validate(self, data: str) -> bool:
        if data == "cef":
            return True
        try:
            with open(data, "r", encoding="utf-8") as file:
                return self.resolve(file.readline().strip()) is not None
        except (FileNotFoundError, UnicodeDecodeError):
            return False
