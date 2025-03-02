from abc import ABC, abstractmethod
from typing import Union

from log import Log


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
