from datetime import datetime


class Log:
    """Represents a log entry in the GLA standard format."""

    def __init__(
        self, level: str, module: str, message: str, timestamp: datetime, source: str
    ):
        """Initialize a log entry

        Args:
            level (str): The log level
            module (str): The module name
            message (str): The log message
            timestamp (datetime): The timestamp
            source (str): The source of the log entry
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
