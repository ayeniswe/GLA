"""
The `transformer` module is an abstraction layer for converting a single log item capture in a `.log` file to a `Log` object for further processing.
"""

from plugins.transformer.transformer import Transformer
from plugins.transformer.log4j_transformer import Log4jTransformer

__all__ = [
    "Transformer",
    "Log4jTransformer",
]
