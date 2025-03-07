"""
The `transformer` module is an abstraction layer for converting a single log item capture in a `.log` file to a `Log` object for further processing.
"""

from plugins.transformer.transformer import Transformer

__all__ = [
    "Transformer",
]
