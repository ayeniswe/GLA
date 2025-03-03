import re
from log import Log
from plugins.transformer import Transformer


class LSMM(Transformer):
    """Transforms a `Log4j` log item with the following order:

    `ERROR` `[main]` `class.example` - `Error message goes here`
    """

    @staticmethod
    def transform(line: str):
        match = re.match(
            r"^(ERROR|WARN|INFO|DEBUG|TRACE) \[(\w+)\] (\w+(?:\.\w+)*) - (.+)$",
            line,
        )
        if match:
            (
                level,
                source,
                module,
                message,
            ) = match.groups()
            return Log(
                level,
                module,
                message,
                source=source,
            )
        else:
            return None
