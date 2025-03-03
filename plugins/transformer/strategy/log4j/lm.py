import re
from log import Log
from plugins.transformer import Transformer


class LM(Transformer):
    """Transforms a `Log4j` log item with the following order:

    `ERROR` - `Error message goes here`
    """

    @staticmethod
    def transform(line: str):
        match = re.match(
            r"^(ERROR|WARN|INFO|DEBUG|TRACE) [^\s]* (.+)$",
            line,
        )
        if match:
            (
                level,
                message,
            ) = match.groups()
            print(level, message)
            return Log(
                level,
                message=message,
            )
        else:
            return None
