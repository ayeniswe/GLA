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
                        r"^(?P<size>\d+) (?P<time>\d+(?:\.\d*)) (?P<type>[rR]) (?P<dir>[rs]) (?P<seq>[\w-]+) (?:(?P<uri>[^\s]+)|-) (?P<dest>[\w.:\]\[]+:\d+:(?:udp|sctp|tls|tcp)) (?P<src>[\w.:\]\[]+:\d+:(?:udp|sctp|tls|tcp)) (?P<to>[^\s]+) (?P<from>[^\s]+) (?P<call>[^\s]+) (?:(?P<status>\d+)|-) (?P<stx>[^\s]+) (?P<ctx>[^\s]+)"
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

            if res.get("dir") == "r":
                msg += " Sent a "
            else:
                msg += " Received a "

            msg += res.get("seq")
            if res.get("type") == "R":
                msg += " request"
            else:
                msg += " response"

            dest = res.get("dest")
            req_uri = res.get("uri")
            if req_uri != dest and req_uri != None:
                msg += f" to {req_uri} ({res.get('dest')})"
            else:
                msg += f" to {res.get('to')} ({res.get('dest')})"

            src = res.get("src")
            msg += f" from {res.get('from')} ({src})"

            return Log(
                source=src,
                timestamp=dateparser.parse(res.get("time"), settings={'TIMEZONE':'UTC'}),
                message=msg,
            )

    def _validate(self, path: PathLike) -> bool:
        with open(path, "r") as file:
            return self.resolve(file.readline().strip()) is not None

# 1: 172 1275930743.699 R s REGISTER-1 sip:example.com 198.51.100.10:5060:udp 198.51.100.1:5060:udp
# sip:example.com sip:alice@example.com;tag=76yhh f81-d4-f6@example.com - - c-tr-1
# 2: 173 1275930744.100 r r REGISTER-1 - 198.51.100.1:5060:udp 198.51.100.10:5060:udp
# sip:example.com;tag=reg-1xtr sip:alice@example.com;tag=76yhh f81-d4-f6@example.com 200 - c-tr-1
# 3: 175 1275930743.699 R r INVITE-43 sip:bob@example.net 203.0.113.200:5060:udp
# 198.51.100.1:5060:udp sip:bob@example.net sip:alice@example.com;tag=a1-1 tr-88h@example.com - s-1-tr -
# Subject,13,"Call me ASAP!"
# 4: 159 1275930744.001 r s INVITE-43 - 198.51.100.1:5060:udp 203.0.113.200:5060:udp sip:bob@example.net
# sip:alice@example.com;tag=a1-1 tr-88h@example.com 100 s-1-tr -
# 5: 184 1275930744.998 R s INVITE-43 sip:bob@bob1.example.net 203.0.113.1:5060:udp 203.0.113.200:5060:udp
# sip:bob@example.net sip:alice@example.com;tag=a1-1 tr-88h@example.com - s-1-tr c-1-tr
# 6: 186 1275930745.500 R s INVITE-43 sip:bob@bob2.example.net [2001:db8::9]:5060:udp 203.0.113.200:5060:udp
# sip:bob@example.net sip:alice@example.com;tag=a1-1 tr-88h@example.com - s-1-tr c-2-tr
# 7: 172 1275930745.800 r r INVITE-43 - 203.0.113.200:5060:udp 203.0.113.1:5060:udp sip:bob@example.net;tag=b1-1
# sip:alice@example.com;tag=a1-1 tr-88h@example.com 100 s-1-tr c-1-tr
# 8: 174 1275930746.100 r r INVITE-43 - 203.0.113.200:5060:udp [2001:db8::9]:5060:udp sip:bob@example.net;tag=b2-2
# sip:alice@example.com;tag=a1-1 tr-88h@example.com 100 s-1-tr c-2-tr
# 9: 174 1275930746.700 r r INVITE-43 - 203.0.113.200:5060:udp [2001:db8::9]:5060:udp sip:bob@example.net;tag=b2-2
# sip:alice@example.com;tag=a1-1 tr-88h@example.com 180 s-1-tr c-2-tr
# 10: 170 1275930746.990 r s INVITE-43 - 198.51.100.1:5060:udp 203.0.113.200:5060:udp sip:bob@example.net;b2-2
# sip:alice@example.com;tag=a1-1 tr-88h@example.com 180 s-1-tr c-2-tr
# 11: 170 1275930747.100 r r INVITE-43 203.0.113.200:5060:udp 203.0.113.1:5060:udp sip:bob@example.net;tag=b1-1
# sip:alice@example.com;tag=a1-1 tr-88h@example.com 180 s-1-tr c-1-tr