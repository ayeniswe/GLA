"""
The `analyzer` module is responsible for analyzing log messages based on predefined criteria.
"""


from pathlib import Path

from gla.analyzer.search.search import StrMatch
from gla.plugins.transformer.cef_transformer import CefTransformer
from gla.plugins.transformer.json_transformer import JsonTransformer
from gla.plugins.transformer.log4j_transformer import Log4jTransformer
from gla.plugins.transformer.ncsa_transformer import NcsaTransformer
from gla.plugins.transformer.sip_transformer import SipTransformer
from gla.plugins.transformer.syslog_transformer import SyslogTransformer
from gla.plugins.transformer.transformer import BaseTransformer, Transformer
from gla.plugins.transformer.xml_transformer import XMLTransformer
from gla.testcase.testcase import TestCase


class Analyzer:
    def __init__(self, testcase: TestCase, file: Path, custom_transformer = None):
        self.testcase = testcase
        self.file = file
        # Always use user defined template first
        self.current_transformer = custom_transformer
        # Support different logging styles
        self.transformers = Transformer(
            [
                JsonTransformer(),
                SyslogTransformer(),
                Log4jTransformer(),
                NcsaTransformer(),
                SipTransformer(),
                CefTransformer(),
                # XMLTransformer(), NOT SUPPORTED YET
            ]
        )
    
    def _setup_transformer(self) -> BaseTransformer:
        """
        Sets up the transformer for processing the current file, if not already set.
        """
        if not self.current_transformer:
            self.current_transformer = self.transformers.get_transformer(self.file)
        
    def _process_line(self, line: str, matcher: StrMatch):        
        """
        Processes a line of text and checks for matches based on the test case criteria.
        """
        result = matcher.search_substr_count(line)
        if result:
            matches = []
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
        self._setup_transformer()
        matcher = StrMatch(self.testcase.patterns)
        
        with open(self.file, "r") as f:
            buffer = ""
            
            # Once all entries are found the search can end early
            line = f.readline()
            while line and len(self.testcase.entries) > 0:
                # Some log message could expand multiple lines
                if line is not '\n':
                    buffer += line
                else:
                    transformed_line = self.current_transformer.transform(buffer)
                    if self._process_line(transformed_line.message, matcher) is None:
                        break
                    buffer = ""
                    
                line = f.readline()