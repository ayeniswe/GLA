"""
The `iterator` module defines iterator strategy to parse though log messages
rather structured or unstructured
"""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from xml.etree.ElementTree import iterparse
from gla.plugins.resolver.resolver import BaseResolver, Resolver
from gla.typings.alias import FileDescriptorOrPath

class Breaker:
    """
    The `Breaker` class represents the delimiter used to split unstructured log data
    into individual log entries.
    """
    
    @property
    def breaker(self) -> str:
        return "\n"

class UnstructuredMixIn(ABC):

    @property
    @abstractmethod
    def breaker() -> str:
        ...

class UnstructuredResolverBreakerMixIn(BaseResolver, UnstructuredMixIn):
    
    @property
    def breaker(self):
        if isinstance(self.strategy, Breaker):
            return self.strategy.breaker
        raise AttributeError("No valid strategy with a breaker has been selected.")

class StructuredMixIn(ABC):

    @property
    @abstractmethod
    def mode() -> str:
        ...

class Unstructured(Iterator):
    """
    The `Unstructured` iterator class that processes log files line by line, with the
    ability to handle multi-line log entries.
    """

    def __init__(self, file: FileDescriptorOrPath, encoding: str, breaker: str):
        self.breaker = breaker
        self.encoding = encoding
        self.file = file

    def __iter__(self):
        self.reader = open(self.file, "r", encoding=self.encoding)
        return self

    def __next__(self):
        line = self.reader.readline()

        if not line:
            self.reader.close()
            raise StopIteration

        # Some log message could expand multiple lines
        buffer = ""
        while line is not self.breaker:
            buffer += line
            line = self.reader.readline()
            # Some files may not end in breaker
            if not line:
                break

        return buffer


class XMLStructure(Iterator):
    def __init__(self, path: FileDescriptorOrPath):
        self.file = path

    def __iter__(self):
        self.reader = iterparse(self.file)
        return self

    def __next__(self):
        return self.reader.__next__()[1]
