"""
The `iterator` module defines iteratoe strategy to parse though log messages
rather structured or unstructured
"""

from collections.abc import Iterator
from xml.etree.ElementTree import iterparse

from gla.typings.alias import FileDescriptorOrPath


class UnstructuredLogProcessor(Iterator):
    """
    The `UnstructuredLogProcessor` iterator class that processes log files line by line, with the
    ability to handle multi-line log entries.
    """

    def __init__(self, file: FileDescriptorOrPath, encoding: str, breakentry="\n"):
        self.breakentry = breakentry
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
        while line is not self.breakentry:
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
