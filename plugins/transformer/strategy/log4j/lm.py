import re
from log import Log
from plugins.transformer import Transformer
from plugins.transformer.transformer import DIVIDER_RE, LEVEL_RE, MSG_RE


class LM(Transformer):
    """Transforms a `Log4j` log item with the following order:

    `ERROR` - `Error message goes here`
    """

    @staticmethod
    def transform(line: str):
        match = re.match(
            rf"{LEVEL_RE} {DIVIDER_RE} {MSG_RE}",
            line,
        )
        if match:
            return Log(
                level=match["lvl"],
                message=match["msg"],
            )
        else:
            return None
