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
)


class LSMM(Transformer):
    """Transforms a `Log4j` log item with the following order:

    `ERROR` `[main]` `class.example` - `Error message goes here`
    """

    @staticmethod
    def transform(line: str):
        match = re.match(
            rf"{LEVEL_RE} {SOURCE_RE} {MODULE_RE} {DIVIDER_RE} {MSG_RE}",
            line,
        )
        if match:
            return Log(
                level=match["lvl"],
                module=match["mod"],
                source=match["src"],
                message=match["msg"],
            )
        else:
            return None
