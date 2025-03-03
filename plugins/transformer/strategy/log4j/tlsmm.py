import re
import dateparser
from log import Log
from plugins.transformer.transformer import (
    Transformer,
    DIVIDER_RE,
    LEVEL_RE,
    MODULE_RE,
    MSG_RE,
    SOURCE_RE,
    TIME_RE,
)


class TLSMM(Transformer):
    """Transforms a `Log4j` log item with the following order:

    `2020-01-01 12:34:56.789` `ERROR` `[main]` `class.example` - `Error message goes here`
    """

    @staticmethod
    def transform(line: str):
        match = re.match(
            rf"{TIME_RE} {LEVEL_RE} {SOURCE_RE} {MODULE_RE} {DIVIDER_RE} {MSG_RE}",
            line,
        )
        if match:
            return Log(
                level=match["lvl"],
                module=match["mod"],
                source=match["src"],
                timestamp=dateparser.parse(match["time"]),
                message=match["msg"],
            )
        else:
            return None
