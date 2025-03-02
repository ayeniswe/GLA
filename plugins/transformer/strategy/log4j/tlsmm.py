import re
from datetime import datetime
from log import Log
from plugins.transformer import Transformer


class TLSMM(Transformer):
    """Transforms a `Log4j` log item with the following order:

    `2020-01-01 12:34:56.789` `ERROR` `[main]` `class.example` - `Error message goes here`
    """

    @staticmethod
    def transform(line: str):
        match = re.match(
            r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}) (ERROR|WARN|INFO|DEBUG|TRACE) \[(\w+)\] (\w+(?:\.\w+)*) - (.+)$",
            line,
        )
        if match:
            (
                timestamp,
                level,
                source,
                module,
                message,
            ) = match.groups()
            return Log(
                level,
                module,
                message,
                datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f"),
                source,
            )
        else:
            return None
