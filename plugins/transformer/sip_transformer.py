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
class SipTransformer(BaseTransformer, Resolver):
    """
    The `SipTransformer` class is responsible for handling transformation
    of `sip` common log messages
    """

    def __init__(self, cache: bool = False):
        """Create a new `SipTransformer`

        NOTE: cache set to `True` will enable the use of the same strategy for
        future log entries seen by this instance
        """
        super().__init__(
            [
                # SIP CLF
                RegexStrategy(
                    compile(
                        r"^(?P<size>\d+) (?P<time>\d+(?:\.\d*)) (?P<type>[rR]) (?P<dir>[rs]) (?P<seq>[\w-]+) (?:-|(?P<uri>[^\s]+)) (?P<dest>[\w.:\]\[]+:\d+:(?:udp|sctp|tls|tcp)) (?P<src>[\w.:\]\[]+:\d+:(?:udp|sctp|tls|tcp)) (?P<to>[^\s]+) (?P<from>[^\s]+) (?P<call>[^\s]+) (?:(?P<status>\d+)|-) (?:-|(?P<stx>[^\s]+)) (?:-|(?P<ctx>[^\s]+))"
                    )
                )
            ],
            cache,
        )

    def _transform(self, entry: str) -> Optional[Log]:
        match: Optional[Match[str]] = self.resolve(entry)
        if match:
            res = match.groupdict()

            # Building a custom message to better promote readability
            msg = f"Session: {res.get('call')} -"
            if res.get("dir") == "s":
                msg += " Sent a "
            else:
                msg += " Received a "
            msg += res.get("seq")
            status = res.get("status")
            if status is not None:
                msg += f" {status}"
            if res.get("type") == "R":
                msg += " request"
            else:
                msg += " response"
            src = res.get("src")
            msg += f" from {res.get('from')} ({src})"
            dest = res.get("dest")
            req_uri = res.get("uri")
            if req_uri != dest and req_uri is not None:
                msg += f" to {req_uri} ({res.get('dest')})"
            else:
                msg += f" to {res.get('to')} ({res.get('dest')})"

            return Log(
                source=src,
                timestamp=dateparser.parse(
                    res.get("time"), settings={"TIMEZONE": "UTC"}
                ),
                message=msg,
            )

    def _validate(self, path: PathLike) -> bool:
        with open(path, "r") as file:
            return self.resolve(file.readline().strip()) is not None

