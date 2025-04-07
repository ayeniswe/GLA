"""
The `strategy` module defines abstract and concrete strategy classes that implement
various strategies, including matching and scoring.
"""
from abc import ABC, abstractmethod
from typing import Any, Match, Optional, Pattern, Tuple


class Strategy(ABC):
    """
    The `Strategy` is an abstract class to promote
    strategies
    """

    @abstractmethod
    def match(self, entry: Any) -> Optional[Any]:
        """Match the entry against the strategy"""
        ...

class StrategyAction(Strategy):
    """
    The `StrategyAction` is an abstract class to promote
    strategies that execute a given command
    """

    @abstractmethod
    def do_action(self, entry: Any) -> Optional[Any]:
        """Execute any given action for strategy"""
        ...


class ScoringStrategy(ABC):
    """
    The `ScoringStrategy` is an abstract class to promote
    scoring strategies
    """

    @abstractmethod
    def score(self, entry: Any) -> Tuple[int, Any]:
        """Score the entry against the strategy"""
        ...

class ScoringStrategyAction(ScoringStrategy):
    """
    The `ScoringStrategyAction` is an abstract class to promote
    scoring strategies that execute a given command
    """

    @abstractmethod
    def do_action(self, entry: Any) -> Optional[Any]:
        """Execute any given action for strategy"""
        ...


class RegexStrategy(Strategy):
    """
    The `RegexStrategy` class is responsible for handling strategies
    based on pre-compiled regular expressions
    """

    def __init__(self, pattern: Pattern):
        self._pattern = pattern

    def match(self, entry: str) -> Optional[Match[str]]:
        return self._pattern.match(entry)
