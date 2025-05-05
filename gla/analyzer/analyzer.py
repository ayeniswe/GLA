"""
The `analyzer` module is responsible for analyzing log messages based on predefined criteria.
"""


from copy import deepcopy
import cchardet

from gla.analyzer.engine import Engine
from gla.analyzer.search.search import StrMatch
from gla.output import console
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
from gla.utilities.result import Result
import logging

logger = logging.getLogger(__name__)

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
        Encoding will auto-resolve.
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
        self.findings = deepcopy(testcase.entries)
        self.file = path
        self.encoding = encoding if encoding else self._detect_encoding(self.file)
        # Always use user defined template first
        self.current_transformer = (
            custom_transformer
            if custom_transformer
            else Transformer(
                [
                    JsonTransformer(),
                    SyslogTransformer(),
                    Log4jTransformer(),
                    NcsaTransformer(),
                    SipTransformer(),
                    CefTransformer(),
                    XMLTransformer(),
                    XMLFragmentTransformer(),
                ]
            ).get_transformer(self.file, self.encoding)
        )

    def _detect_encoding(self, filename: FileDescriptorOrPath) -> str:
        """Detect encoding and reject confidence levels below 99%"""
        detection = cchardet.detect(open(filename, "rb").read(4))
        if detection["confidence"] > 0.99:
            return detection["encoding"]
        raise UnicodeError("failed to auto-detect encoding. Please specify encoding to use")

    def _process_entry(self, line_num: int, log_entry: str, matcher: StrMatch) -> int:
        """
        Processes a log entry and checks for matches based on the test case criteria.

        Modifies the test case entries in-place
        """
        # All substrings that can be located in the current piece of text
        matches = matcher.search_substr(log_entry)
        if matches:
            # At most, only a few matches should be returned—typically just one on average.
            # In practice, this results in closer to O(n) complexity, since every log line
            # still needs to be parsed.
            logger.debug(f"ENTRY {line_num}: found substrings: {matches}")
            for match in matches:
                if match in self.findings:
                    entry = self.testcase.entries[match]
                    
                    # Some entries may need to be seen multiple times
                    # to validate passing
                    logger.debug(f"dropping the count of an entry: {match}")
                    self.findings[match].val.cnt -= 1
                    cnt = self.findings[match].val.cnt

                    # We no longer need to track entries that are found
                    # they can...poof disappear
                    if cnt == 0:
                        logger.debug(f"dumping a entry: {match}")
                        del self.findings[match]
                    # Some matches should never appear the
                    # only logical way to arrive here is
                    # if the entry is testing absences
                    elif cnt == -1:
                        logger.debug(f"failed to not find entry: {match}")
                        return Result.Error
                    
                    # Previous test should always pass current test
                    # when sequential mode is on
                    if entry.prev and self.testcase.seq:
                        if self.findings.get(entry.prev.val.text):
                            logger.debug(f"failed to find previous entry: {entry.prev.val.text}")
                            return Result.Error
        else:
            logger.debug(f"ENTRY {line_num}: nothing found")

        return Result.Ok

    def _run(self):
        matcher = StrMatch(self.testcase.patterns)
        for i, log_entry in enumerate(Engine(self.file, self.encoding, self.current_transformer)):
            # Once all entries are found the search can end early
            if len(self.testcase.entries) == 0:
                logger.debug(f"all entries found")
                break

            result = Result.Ok
            transformed_log_entry = self.current_transformer.transform(log_entry)
            if transformed_log_entry:
                result = self._process_entry(i, transformed_log_entry.message, matcher)
            else:
                logger.debug(f"ENTRY {i}: skipping transformation - {log_entry}")
                result = self._process_entry(i, log_entry, matcher)
            # Fail early to avoid full log search
            if result is Result.Error:
                break

        # Share results
        console.show(self.findings, self.testcase.entries, self.testcase.seq)