import time
from gla.analyzer.analyzer import Analyzer
from gla.plugins.transformer.syslog_transformer import SyslogTransformer
from gla.testcase.testcase import TestCase
from lxml.etree import iterparse, XMLSyntaxError

file_path = "gla/plugins/transformer/tests/logs/test-syslog.log"
t = TestCase()
a = Analyzer(t, file_path)
a.run()