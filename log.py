from datetime import datetime
from typing import Union


class Log:
    """Represents a log entry in the GLA standard format."""

    def __init__(
        self,
        level: Union[str, None] = None,
        module: Union[str, None] = None,
        message: Union[str, None] = None,
        timestamp: Union[datetime, None] = None,
        source: Union[str, None] = None,
    ):
        """Initialize a log entry

        Args:
            level (str | None): The log level
            module (str | None): The module name
            message (str | None): The log message
            timestamp (datetime | None): The timestamp
            source (str | None): The source of the log entry
        """
        self._level = level
        self._module = module
        self._message = message
        self._timestamp = timestamp
        self._source = source

    def __eq__(self, value):
        return isinstance(value, Log) and (
            self._level == value._level
            and self._module == value._module
            and self._message == value._message
            and self._timestamp == value._timestamp
            and self._source == value._source
        )

    def __str__(self):
        return f"{self._timestamp.isoformat()} {self._level} [{self._source}] {self._module} - {self._message}"
