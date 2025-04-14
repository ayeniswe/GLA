from json import JSONDecodeError, loads
import time
from gla.analyzer.analyzer import Analyzer
from gla.analyzer.iterator import JSONStructure, Mode, Structured
from gla.plugins.transformer.sip_transformer import SipTransformer
from gla.plugins.transformer.syslog_transformer import SyslogTransformer
from gla.plugins.transformer.tests.conftest import get_log_path
from gla.plugins.transformer.transformer import Transformer
from gla.testcase.testcase import TestCase
from lxml.etree import iterparse, XMLSyntaxError

file_path = "gla/plugins/transformer/tests/logs/test-json.log"
file_path = "gla/plugins/transformer/tests/logs/test-sip.log"
# t = TestCase()
# a = Analyzer(t, file_path)
# a.run()