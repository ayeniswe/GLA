"""
The `alias` module contains commonly used type aliases
"""

from os import PathLike
from typing import Union

FileDescriptorOrPath = Union[int, str, bytes, PathLike]
