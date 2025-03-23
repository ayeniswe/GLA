import os

from pytest import raises

from plugins.transformer import Transformer
from plugins.transformer.cef_transformer import CefTransformer
from plugins.transformer.json_transformer import JsonTransformer
from plugins.transformer.log4j_transformer import Log4jTransformer
from plugins.transformer.ncsa_transformer import NcsaTransformer
from plugins.transformer.sip_transformer import SipTransformer
from plugins.transformer.syslog_transformer import SyslogTransformer
from plugins.transformer.xml_transformer import XMLTransformer


def test_transformer_factory():
    trans = Transformer(
        [
            JsonTransformer(),
            SyslogTransformer(),
            Log4jTransformer(),
            XMLTransformer(),
            NcsaTransformer(),
            SipTransformer(),
            CefTransformer(),
        ]
    )
    result = trans.get_transformer(
        os.path.join(os.path.dirname(__file__), "logs", "test-log4j.log")
    )
    assert isinstance(result, Log4jTransformer), "Should resolve as log4j transformer"
    result = trans.get_transformer(os.path.join(os.path.dirname(__file__), "logs", "test-jlu.log"))
    assert isinstance(result, XMLTransformer), "Should resolve as xml transformer"
    result = trans.get_transformer(os.path.join(os.path.dirname(__file__), "logs", "test.xml"))
    assert isinstance(result, XMLTransformer), "Should resolve as xml transformer"
    result = trans.get_transformer(
        os.path.join(os.path.dirname(__file__), "logs", "test-syslog.log")
    )
    assert isinstance(result, SyslogTransformer), "Should resolve as syslog transformer"
    result = trans.get_transformer(os.path.join(os.path.dirname(__file__), "logs", "test-sip.log"))
    assert isinstance(result, SipTransformer), "Should resolve as sip transformer"
    result = trans.get_transformer(os.path.join(os.path.dirname(__file__), "logs", "test-ncsa.log"))
    assert isinstance(result, NcsaTransformer), "Should resolve as ncsa transformer"
    result = trans.get_transformer(os.path.join(os.path.dirname(__file__), "logs", "test-cef.log"))
    assert isinstance(result, CefTransformer), "Should resolve as cef transformer"


def test_transformer_factory_undetermined():
    trans = Transformer(
        [
            JsonTransformer(),
            SyslogTransformer(),
            Log4jTransformer(),
            XMLTransformer(),
            NcsaTransformer(),
            SipTransformer(),
            CefTransformer(),
        ]
    )
    with raises(ValueError, match="transformer could not be determined"):
        trans.get_transformer(os.path.join(os.path.dirname(__file__), "logs", "test-unk.log"))
