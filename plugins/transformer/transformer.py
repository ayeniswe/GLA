from abc import ABC, abstractmethod
from typing import Union

from log import Log

# Supports the division between two attributes in log message
# rather that division exists or doesn't
DIVIDER_RE = r"[^\s]*"
# Supports the gathering timestamps in log messages
TIME_RE = r"(?P<time>(?:\d{2,4}-\d{2,4}-\d{2,4})*[T\s]*(\d{2}:\d{2}:\d{2}(?:.\d{3})*)*)"
# Supports the gathering of common levels in log messages
LEVEL_RE = r"[^a-zA-Z\s]*(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)[^a-zA-Z\s]*"
# Support the gathering of abritrary log messages
MSG_RE = r"(?P<msg>.+)"
# Supports the gathering of any inner casing for the module or source in log message
# and allows $, -, . characters to be used in that module or source
SOURCE_RE = r"[^a-zA-Z\s]*(?P<src>[\w$.]+)[^a-zA-Z\s]*"
MODULE_RE = r"[^a-zA-Z\s]*(?P<mod>[\w$.]+)[^a-zA-Z\s]*"


class Transformer(ABC):
    """
    Abstract base class for transformers
    """

    @abstractmethod
    def transform(line: str) -> Union[Log, None]:
        """Transform a line

        Args:
            line (str): a line of text to transform

        Returns:
            Log: the GLA log standard format or `None` if the format can not be determined
        """
        ...
