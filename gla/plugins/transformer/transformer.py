"""
The `transformer` module is an abstract class designed to allow extensibility for
log transformation. It serves as the base class for creating log transformers
that convert log entries into structured `Log` objects and validate log files.
"""
from abc import abstractmethod
from typing import Any, List, Optional

from gla.models.log import Log
from gla.plugins.validator.validator import Validator


class BaseTransformer:
    """
    The `BaseTransformer` is an abstract class to promote
    transformers extensibility and factory use
    """

    @abstractmethod
    def transform(self, entry: Any) -> Optional[Log]:
        """Transforms a log entry into a `Log` object

        Args:
            entry (Any): a log entry to transform
        """

class BaseTransformerValidator(BaseTransformer, Validator):
    ...

class Transformer:
    """
    The `Transformer` class is responsible for handling transformation logic of log
    messages
    """

    def __init__(self, transformers: List[BaseTransformerValidator]):
        self._transformers = transformers

    def get_transformer(self, data: str) -> BaseTransformer:
        """Get a transformer to process log messages

        Args:
            data (str): input data to validate against

        Raises:
            ValueError: if a transformer cannot be determined
        """
        for transformer in self._transformers:
            if transformer.validate(data):
                return transformer
        raise ValueError("transformer could not be determined")
