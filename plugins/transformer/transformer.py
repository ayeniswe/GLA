from abc import ABC, abstractmethod
from os import PathLike
from pathlib import Path
from typing import List, Optional
from typeguard import typechecked
from models.log import Log


@typechecked
class BaseTransformer(ABC):
    """
    The `BaseTransformer` is an abstract class to promote
    transformers extensibility and factory use
    """

    @abstractmethod
    def _transform(self, entry: str) -> Optional[Log]:
        """Transforms a log entry into a `Log` object

        Args:
            entry (str): a log entry to transform
        """

    @abstractmethod
    def _validate(self, path: PathLike) -> bool:
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
            if transformer._validate(Path(path)):
                return transformer
        raise ValueError("transformer could not be determined")
