"""
The `transformer` module is an abstraction layer for converting a single log item capture in a `.log` file to the `GLA` standard.
"""

from .transformer import Transformer
from .strategy.sslcerts import SslcertsTransformer
from .strategy.default import DefaultTransformer

__all__ = ["Transformer", "SslcertsTransformer", "DefaultTransformer"]
