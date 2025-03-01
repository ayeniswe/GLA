from abc import ABC, abstractmethod

class Transformer(ABC):
    """
    Abstract base class for transformers.
    """
    @abstractmethod
    def transform(self, line: str) -> str:
        ...