"""
The `transformer` module is an abstraction layer for converting a single log item capture in a
`.log` file to a `Log` object for further processing.
"""

from gla.plugins.transformer.transformer import Transformer
from gla.plugins.transformer.custom_transformer import CustomTransformer

__all__ = [
    "Transformer",
    "CustomTransformer",
]
