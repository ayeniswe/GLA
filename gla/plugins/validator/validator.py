"""
The `validator` module provides base classes for validating various inputs
"""


from abc import ABC, abstractmethod
from typing import Any


class Validator(ABC):
    """
    The `Validator` is an abstract class to validate input
    """

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate some input data

        Args:
            data (Any): input data to validate against
        """
