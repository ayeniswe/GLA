"""
The `transformer` module is an abstract class designed to allow extensibility for
log transformation. It serves as the base class for creating log transformers
that convert log entries into structured `Log` objects and validate log files.
"""
from abc import ABC, abstractmethod
from os import PathLike
from pathlib import Path
from typing import Any, List, Optional

from typeguard import typechecked

from models.log import Log


@typechecked
class BaseTransformer(ABC):
    """
    The `BaseTransformer` is an abstract class to promote
    transformers extensibility and factory use
    """

    @abstractmethod
    def _transform(self, entry: Any) -> Optional[Log]:
        """Transforms a log entry into a `Log` object

        Args:
            entry (Any): a log entry to transform
        """

    @abstractmethod
    def validate(self, path: PathLike) -> bool:
        """Validate if a log file is parseable

        Args:
            path (Path): a path to a log file
        """


@typechecked
class Transformer:
    """
    The `Transformer` class is responsible for handling transformation logic of log
    messages
    """

    def __init__(self, transformers: List[BaseTransformer]):
        self._transformers = transformers

    def get_transformer(self, path: str) -> BaseTransformer:
        """Get a transformer to process log messages

        Raises:
            ValueError: if a transformer cannot be determined
        """
        for transformer in self._transformers:
            if transformer.validate(Path(path)):
                return transformer
        raise ValueError("transformer could not be determined")
