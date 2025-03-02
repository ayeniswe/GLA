import re
from datetime import datetime
from log import Log
from plugins.transformer import Transformer


class TSLMM(Transformer):
    """Transforms a `Log4j` log item with the following order:

    `2020-01-01 12:34:56.789` `[main]` 'ERROR` class.example` - `Error message goes here`
    """

    @staticmethod
    def transform(line: str):
        match = re.match(
            r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}) \[(\w+)\] (ERROR|WARN|INFO|DEBUG|TRACE) (\w+(?:\.\w+)*) - (.+)$",
            line,
        )
        if match:
            (
                timestamp,
                source,
                level,
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
