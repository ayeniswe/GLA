"""
The `validator` module provides base classes for validating various inputs
"""


from abc import ABC, abstractmethod
from typing import Any, Dict


class Validator(ABC):
    """
    The `Validator` is an abstract class to validate input
    """

    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate some input data

        Args:
            data (dict[str, Any]): input data to validate against
        """
