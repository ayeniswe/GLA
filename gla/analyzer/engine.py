"""
The `engine` module is responsible for processing the logs and handling any side effects
or optional task needed
"""

from typing import Iterator
from gla.analyzer.iterator import Structured, StructuredMixIn, Unstructured, UnstructuredMixIn
from gla.plugins.transformer.transformer import BaseTransformer
from gla.typings.alias import FileDescriptorOrPath


class Engine(Iterator):
    def __init__(self, path: FileDescriptorOrPath, encoding: str, transformer: BaseTransformer):
        self.transformer = transformer
        self.file = path
        self.encoding = encoding
        if isinstance(self.transformer, UnstructuredMixIn):
            self.iterator = Unstructured(self.file, self.encoding, self.transformer.breaker)
        elif isinstance(self.transformer, StructuredMixIn):
            self.iterator = Structured(self.file, self.encoding, self.transformer.mode)
        
    def __iter__(self):
        return self.iterator.__iter__()
    
    def __next__(self):
        return self.iterator.__next__()