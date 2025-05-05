"""
The `testcase` module provides functionality to define and manage test cases
for evaluating log entries.
"""

from typing import List, Tuple, Union

from gla.models.entry import Entry
from pydantic import Field

from gla.models.criteria import Criteria
    

class TestCase(Criteria):
    """
    Represents a handmade test case for log entry matching based on predefined criteria.

    The `TestCase` class allows the user to define a set of fuzzy matching and search criteria that
    can be used to validate the presence or absence of certain patterns or conditions in logs.
    By default, log entries are treated as non-sequential, meaning their order
    in the log doesn't matter. However, if the order of entries is important, the `seq=True`
    argument can be used to make the entries sequential, meaning the entries will need to appear
    in the specified order
    """

    name: Union[str, None] = Field(default=None, description="The name of the test case")
    """The name of the test case"""
    patterns: List[str] = Field(default=list(), description="The substring patterns to search for")
    """The substring patterns to search for"""
    seq: bool = Field(
        default=False,
        description="Rather to process test case sequentially. \
        Fails fast if entries do not appear in order specified",
    )
    """
    Rather to process test case sequentially.
    Fails fast if entries do not appear in order specified
    """

    def find_entries(self, entry: Union[List[str], str]):
        """Add a single or multiple log entries to the search criteria where order is irrelevant"""
        if isinstance(entry, list):
            for e in entry:
                self.find_entries_count((e, 1))
        elif isinstance(entry, str):
            self.find_entries_count((entry, 1))

    def find_entries_count(self, entry: Union[List[Tuple[str, int]], Tuple[str, int]]):
        """
        Add the count of occurrences for a single or multiple log entries to the search
        criteria
        """
        if isinstance(entry, list):
            for e in entry:
                node = self.entries.get(e[0])
                if node:
                    node.val.cnt += e[1]
                else:
                    self.patterns.append(e[0])
                    self.entries[e[0]] = Entry(text=e[0], cnt=e[1])
        elif isinstance(entry, tuple):
            node = self.entries.get(entry[0])
            if node:
                node.val.cnt += entry[1]
            else:
                self.patterns.append(entry[0])
                self.entries[entry[0]] = Entry(text=entry[0], cnt=entry[1])

    def find_entries_absent(self, entry: Union[List[str], str]):
        """Find if a single or multiple log entries are absent from the search criteria"""
        if isinstance(entry, list):
            for e in entry:
                self.find_entries_count((e, 0))
        elif isinstance(entry, str):
            self.find_entries_count((entry, 0))