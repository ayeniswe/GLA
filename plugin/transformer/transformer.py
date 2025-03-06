from abc import ABC, abstractmethod
from typing import Union
from model.log import Log


class Transformer(ABC):
    """
    The `Transformer` is an abstract class for handling transformation logic of log
    messages
    """

    @abstractmethod
    def transform(self, line: str) -> Union[Log, None]:
        """Transforms a log into a `Log` object

        Args:
            line (str): a line of text to transform

        Returns:
            Log: A `Log` object or `None` if the format can not be determined
        """
