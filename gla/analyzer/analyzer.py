"""
The `analyzer` module is responsible for analyzing log messages based on predefined criteria.
"""


from typing import List

import cchardet

from gla.analyzer.iterator import Breaker, Unstructured, XMLStructure
from gla.analyzer.search.search import StrMatch
from gla.plugins.transformer.cef_transformer import CefTransformer
from gla.plugins.transformer.json_transformer import JsonTransformer
from gla.plugins.transformer.log4j_transformer import Log4jTransformer
from gla.plugins.transformer.ncsa_transformer import NcsaTransformer
from gla.plugins.transformer.sip_transformer import SipTransformer
from gla.plugins.transformer.syslog_transformer import SyslogTransformer
from gla.plugins.transformer.transformer import BaseTransformer, Transformer
from gla.plugins.transformer.xml_transformer import XMLTransformer
from gla.plugins.transformer.xmlfragment_transformer import XMLFragmentTransformer
from gla.testcase.testcase import TestCase
from gla.typings.alias import FileDescriptorOrPath

class Analyzer:
    """
    The `Analyzer` class is responsible for processing log files and matching them
    against a set of test case criteria.

    This class provides the ability to transform logs using different transformers
    (e.g., Json, Syslog, Log4j, etc.) and process each line of the log file to check for matches
    based on user-defined patterns.

    Args:
        `testcase` (TestCase): The test case containing the patterns and expected entries
        to match against the log.
        `file` (FileDescriptorOrPath): The log file to be processed (can be a file path or
        file-like object).
        `encoding` (str, optional): The encoding to use when reading the log file.
        Defaults to "utf-8".
        `custom_transformer` (BaseTransformer, optional): A user-defined transformer
        for processing the log data.
        If not provided, a default transformer will be selected based on the file information.
    """

    def __init__(
        self,
        testcase: TestCase,
        path: FileDescriptorOrPath,
        encoding: str = None,
        custom_transformer: BaseTransformer = None,
    ):
        self.testcase = testcase
        self.file = path
        self.encoding = encoding if encoding else self._detect_encoding(self.file)
        # Always use user defined template first
        self.current_transformer = (
            custom_transformer
            if custom_transformer
            else Transformer(
                [
                    # JsonTransformer(),
                    SyslogTransformer(),
                    Log4jTransformer(),
                    # NcsaTransformer(),
                    # SipTransformer(),
                    # CefTransformer(),
                    # XMLTransformer(), # NOT SUPPORTED YET
                    # XMLFragmentTransformer()
                ]
            ).get_transformer(self.file, self.encoding)
        )

    def _detect_encoding(self, filename: FileDescriptorOrPath) -> str:
        """Detect encoding and reject confidence levels below 99%"""
        detection = cchardet.detect(open(filename, "rb").read(4))
        if detection["confidence"] > 0.99:
            return detection["encoding"]
        raise UnicodeError("failed to auto-detect encoding. Please specify encoding to use")

    def _process_line(self, line: str, matcher: StrMatch):
        """
        Processes a line of text and checks for matches based on the test case criteria.
        """
        result = matcher.search_substr_count(line)
        if result:
            matches: List[str] = []
            entries_as_list = list(self.testcase.entries.keys())
            for idx, entry in enumerate(entries_as_list):
                actual_cnt = result.get(entry)
                expected_cnt = self.testcase.entries.get(entry)

                # Fail fast happens when previous
                # entry encounter never happens before current entry
                if idx > 0:
                    prev_text = entries_as_list[idx - 1]
                    exists = self.testcase.entries.get(prev_text)
                    prev_found = result.get(matches[-1]) if len(matches) > 0 else None
                    if exists and self.testcase.seq and prev_found is None and actual_cnt:
                        print(f"Failed here: {entry}")
                        return

                # Match
                if actual_cnt and actual_cnt == expected_cnt:
                    matches.append(entry)
                    print(f"Match found: {entry}")

            # No longer need to track items found
            for match in matches:
                del self.testcase.entries[match]

        # Successful processing
        return 0

    def run(self):
        ...
        # matcher = StrMatch(self.testcase.patterns)

        # for entry in LogProcessor(self.file, self.encoding):
        #     # Once all entries are found the search can end early
        #     if len(self.testcase.entries) == 0:
        #         break

        #     if self._process_line(entry, matcher) is None:
        #         break
