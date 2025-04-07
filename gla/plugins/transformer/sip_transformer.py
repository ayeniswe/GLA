"""
The `sip_transformer` module is responsible for transforming SIP (Session
Initiation Protocol) log entries into structured `Log` objects.
"""
import re
from datetime import datetime, timezone
from typing import Any, Dict, Match, Optional

from gla.analyzer.iterator import UnstructuredBreakerMixIn, UnstructuredResolverBreakerMixIn
from gla.models.log import Log
from gla.plugins.resolver.resolver import Resolver
from gla.plugins.transformer.transformer import BaseTransformerValidator, RegexBreakerStrategy
from gla.typings.alias import FileDescriptorOrPath


class SipTransformer(BaseTransformerValidator, Resolver, UnstructuredResolverBreakerMixIn):
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
                RegexBreakerStrategy(
                    re.compile(
                        r"^(?P<size>\d+) "
                        r"(?P<time>\d+(?:\.\d*)) "
                        r"(?P<type>[rR]) "
                        r"(?P<dir>[rs]) "
                        r"(?P<seq>[\w-]+) "
                        r"(?:-|(?P<uri>[^\s]+)) "
                        r"(?P<dest>[\w.:\]\[]+:\d+:(?:udp|sctp|tls|tcp)) "
                        r"(?P<src>[\w.:\]\[]+:\d+:(?:udp|sctp|tls|tcp)) "
                        r"(?P<to>[^\s]+) "
                        r"(?P<from>[^\s]+) "
                        r"(?P<call>[^\s]+) "
                        r"(?:(?P<status>\d+)|-) "
                        r"(?:-|(?P<stx>[^\s]+)) "
                        r"(?:-|(?P<ctx>[^\s]+))"
                    )
                )
            ],
            cache,
        )

    def transform(self, entry: str) -> Optional[Log]:
        match: Optional[Match[str]] = self.resolve(entry)
        if match:
            res = match.groupdict()

            # Building a custom message to better promote readability
            msg = f"Session: {res.get('call')} -"
            if res.get("dir") == "s":
                msg += " Sent a "
            else:
                msg += " Received a "
            msg += res.get("seq", "")
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

            time = res.get("time")
            timedate = None
            if time is not None:
                dt = datetime.fromtimestamp(float(time), timezone.utc)  # Convert to UTC datetime
                timedate = dt.strftime("%Y-%m-%dT%H:%M:%S")

            return Log(
                source=src,
                timestamp=timedate,
                message=msg,
            )
        return None

    def validate(self, data: Dict[str, Any]) -> bool:
        if data["data"] == "sip":
            return True
        try:
            path: FileDescriptorOrPath = data["data"]
            with open(path, "r", encoding=data["encoding"]) as file:
                return self.resolve(file.readline().strip()) is not None
        except (FileNotFoundError, UnicodeDecodeError):
            return False
