"""
The `transformer` module is an abstract class designed to allow extensibility for
log transformation. It serves as the base class for creating log transformers
that convert log entries into structured `Log` objects and validate log files.
"""
from abc import abstractmethod
from typing import Any, List, Optional, Tuple, Match

from gla.analyzer.iterator import Breaker, Unstructured
from gla.typings.alias import FileDescriptorOrPath
from gla.models.log import Log
from gla.plugins.resolver.resolver import BaseResolver, Resolver
from gla.plugins.validator.validator import Validator
from gla.typings.alias import FileDescriptorOrPath
from gla.utilities.strategy import RegexStrategy, StrategyAction

class RegexBreakerStrategy(RegexStrategy, Breaker, StrategyAction):
    """
    The `RegexBreakerStrategy` strategy for breaking and matching 
    unstructured logs using regular expressions
    """
    def match(self, entry: Tuple[FileDescriptorOrPath, str]) -> Optional[Match[str]]:
        for line in Unstructured(entry[0], entry[1], self.breaker):
            return self._pattern.match(line)
        
    def do_action(self, entry: str):
        return RegexStrategy.match(self, entry)

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

class ResolverBreaker(BaseResolver, Breaker):
    
    @property
    def breaker(self) -> str:
        if isinstance(self.strategy, Breaker):
            return self.strategy.breaker
        raise AttributeError("No valid strategy with a breaker has been selected.")
                             
class BaseTransformerValidator(BaseTransformer, Validator):
    ...

class Transformer:
    """
    The `Transformer` class is responsible for handling transformation logic of log
    messages
    """

    def __init__(self, transformers: List[BaseTransformerValidator]):
        self._transformers = transformers

    def get_transformer(self, data: FileDescriptorOrPath, encoding: str = None) -> BaseTransformer:
        """Get a transformer to process log messages

        Args:
            data (FileDescriptorOrPath): input data to validate against rather a file
            or simple string
            encoding (str): The character encoding of the input data (e.g., 'utf-8', 'ascii', etc.).

        Raises:
            ValueError: if a transformer cannot be determined
        """
        for transformer in self._transformers:
            if transformer.validate({"data": data, "encoding": encoding}):
                return transformer
        raise ValueError("transformer could not be determined")
