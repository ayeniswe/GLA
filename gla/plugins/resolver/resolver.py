"""
The `resolver` module provides classes for resolving log entries based on a list of strategies.
"""

import sys
from abc import ABC, abstractmethod
from typing import Any, List, Optional

from gla.utilities.strategy import ScoringStrategyArtifact, Strategy, StrategyAction


class BaseResolver(ABC):
    """
    The `BaseResolver` is an abstract class to provide
    resolution capabilities
    """

    @abstractmethod
    def resolve(self, entry: Any):
        ...

    @property
    @abstractmethod
    def strategy(self) -> Strategy:
        ...


class Resolver(BaseResolver):
    """
    The `Resolver` is an extension class to extend
    resolution capabilities with a list of strategies
    """

    def __init__(self, strategies: List[StrategyAction], cache: bool):
        """
        Create a new `Resolver`

        NOTE: cache set to `True` will enable the use of the same strategy for
        future log entries seen by this instance
        """
        self._cache = cache
        self._strategies: List[StrategyAction] = strategies
        self._cache_strategy: Optional[StrategyAction] = None

    @property
    def strategy(self) -> Optional[Strategy]:
        return self._cache_strategy

    def resolve(self, entry: Any) -> Optional[Any]:
        """Resolves to the correct strategy for the given entry"""
        if self._cache and self._cache_strategy:
            return self._cache_strategy

        for strategy in self._strategies:
            match = strategy.match(entry)
            if match:
                # Save strategy for redundant uses
                self._cache_strategy = strategy
                return self._cache_strategy
        return None


class BestResolver(BaseResolver):
    """
    The `BestResolver` is an extension class to extend
    resolution capabilities with a "highest scorer" scoring system
    """

    def __init__(self, strategies: List[ScoringStrategyArtifact], cache: bool):
        self._cache = cache
        self._strategies: List[ScoringStrategyArtifact] = strategies
        self._cache_strategy = None

    @property
    def strategy(self) -> Optional[Strategy]:
        return self._cache_strategy

    def resolve(self, entry: Any) -> Any:
        """Resolves to the best strategy based on a "highest scorer" scoring system

        NOTE: No tie-breaker..the chosen strategy is the first seen
        """
        if self._cache and self._cache_strategy:
            return self._cache_strategy

        max_scorer = (-sys.maxsize - 1, None)
        for strategy in self._strategies:
            (max_score, _) = max_scorer
            score = strategy.score(entry)
            if (
                max(
                    max_score,
                    score,
                )
                != max_score
            ):
                max_scorer = (score, strategy)
        # Save strategy result for redundant uses
        self._cache_strategy = max_scorer[1]
        return max_scorer[1]
