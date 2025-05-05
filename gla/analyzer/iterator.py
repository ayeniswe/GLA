"""
The `iterator` module defines iterator strategy to parse though log messages
rather structured or unstructured
"""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from enum import Enum
from json import JSONDecodeError, loads
from typing import Union

from lxml.etree import _Element, iterparse

from gla.plugins.resolver.resolver import BaseResolver
from gla.typings.alias import FileDescriptorOrPath


class Mode(Enum):
    XML = "xml"
    JSON = "json"


class Breaker:
    """
    The `Breaker` class represents the delimiter used to split unstructured log data
    into individual log entries.
    """

    @property
    def breaker(self) -> str:
        return ""


class UnstructuredMixIn(ABC):
    @property
    @abstractmethod
    def breaker(self) -> str:
        ...


class UnstructuredBaseResolverBreakerMixIn(BaseResolver, UnstructuredMixIn):
    @property
    def breaker(self):
        if isinstance(self.strategy, Breaker):
            return self.strategy.breaker
        raise AttributeError("No valid strategy with a breaker has been selected.")


class StructuredMixIn(ABC):
    @property
    @abstractmethod
    def mode(self) -> str:
        ...


class Unstructured(Iterator):
    """
    The `Unstructured` iterator class that processes log files line by line, with the
    ability to handle multi-line log entries.
    """

    def __init__(self, file: FileDescriptorOrPath, encoding: str, breaker: str):
        """
        Initializes the `Unstructured` iterator

        Its important to consider that the `breaker` value is not included in the
        returned value during each iteration

        Args:
            `file` (FileDescriptorOrPath): The log file or file descriptor to process.
            This could be a file path or an open file descriptor.
            `encoding` (str): The encoding used to read the file, such as 'utf-8' or 'latin-1'.
            `breaker` (str): A string that marks the end of a multi-line log entry.
            This string helps the iterator identify where one log entry ends and the next begins.
        """
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
        if self.breaker:
            while line != self.breaker:
                buffer += line
                line = self.reader.readline()
                # Some files may not end in breaker
                if not line:
                    break
        else: 
            buffer = line

        return buffer


class Structured(Iterator):
    """
    Structured log parser that delegates to a format-specific parser based on the given mode.
    """

    def __init__(self, path: FileDescriptorOrPath, encoding: str, mode: Mode):
        self.file = path
        self.encoding = encoding
        self.iterator: Union[XMLStructure, JSONStructure]
        if mode == Mode.XML:
            self.iterator = XMLStructure(self.file, self.encoding)
        elif mode == Mode.JSON:
            self.iterator = JSONStructure(self.file, self.encoding)

    def __iter__(self):
        return self.iterator.__iter__()

    def __next__(self):
        return self.iterator.__next__()


class XMLStructure(Iterator):
    """
    Iterator for parsing XML log files using incremental parsing.
    """

    def __init__(self, path: FileDescriptorOrPath, encoding: str):
        self.file = path
        self.encoding = encoding

    def __iter__(self):
        self.reader = iterparse(self.file, encoding=self.encoding)
        return self

    def __next__(self) -> _Element:
        return self.reader.__next__()[1]


class JSONStructure(Iterator):
    """
    Iterator for parsing JSON log files
    """

    def __init__(self, path: FileDescriptorOrPath, encoding: str):
        self.file = path
        self.encoding = encoding

    def __iter__(self):
        self.reader = open(self.file, "r", encoding=self.encoding)
        return self

    def __next__(self) -> dict:
        line = self.reader.readline()

        if not line:
            self.reader.close()
            raise StopIteration

        try:
            return loads(line)
        except JSONDecodeError:
            # Some JSON is prettify so it will not sit on one line
            buffer = ""
            while line and not line.strip("\n").endswith("}"):
                buffer += line
                line = self.reader.readline()
            return loads(buffer + line)
