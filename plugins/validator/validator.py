"""
The `validator` module provides base classes for validating various inputs
"""


from abc import ABC, abstractmethod

from typeguard import typechecked


@typechecked
class Validator(ABC):
    """
    The `Validator` is an abstract class to validate input
    """

    @abstractmethod
    def validate(self, data: str) -> bool:
        """Validate some input data

        Args:
            data (str): input data to validate against
        """
