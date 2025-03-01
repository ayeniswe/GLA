from abc import ABC
from typing import Any, Pattern, Optional, Match, Tuple
from typeguard import typechecked


@typechecked
class Strategy(ABC):
    """
    The `Strategy` is an abstract class to promote
    strategies
    """

    def match(self, entry: Any) -> Optional[Any]:
        """Match the entry against the strategy"""
        ...


@typechecked
class ScoringStrategy(ABC):
    """
    The `ScoringStrategy` is an abstract class to promote
    scoring strategies
    """

    def score(self, entry: Any) -> Tuple[int, Any]:
        """Score the entry against the strategy"""
        ...


@typechecked
class RegexStrategy(Strategy):
    """
    The `RegexStrategy` class is responsible for handling strategies based on pre-compiled regular expressions
    """

    def __init__(self, pattern: Pattern):
        self._pattern = pattern

    def match(self, entry: str) -> Optional[Match[str]]:
        return self._pattern.match(entry)
