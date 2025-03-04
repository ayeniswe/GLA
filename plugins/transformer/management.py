from typing import List
from plugins.transformer.transformer import Transformer


class Management:
    """
    The `Management` class is responsible for dynamically resolving formatting
    strategies with logs
    """

    def __init__(self, strategies: List[Transformer]):
        """
        Initialize a list of available strategies
        """
        self._strategies = strategies

    def resolve(self, line: str) -> Transformer:
        """
        Resolve the appropriate formatting strategy for the given log
        """
        for strategy in self._strategies:
            if strategy.transform(line):
                return strategy
        return None
