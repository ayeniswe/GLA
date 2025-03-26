import os

from plugins.transformer import Transformer
from plugins.transformer.cef_transformer import CefTransformer
from plugins.transformer.json_transformer import JsonTransformer
from plugins.transformer.log4j_transformer import Log4jTransformer
from plugins.transformer.ncsa_transformer import NcsaTransformer
from plugins.transformer.sip_transformer import SipTransformer
from plugins.transformer.syslog_transformer import SyslogTransformer
from plugins.transformer.xml_transformer import XMLTransformer
from pytest import raises


def test_transformer_factory_by_path():
    trans = Transformer(
        [
            JsonTransformer(),
            SyslogTransformer(),
            Log4jTransformer(),
            NcsaTransformer(),
            SipTransformer(),
            CefTransformer(),
            XMLTransformer(),
        ]
    )
    result = trans.get_transformer(
        os.path.join(os.path.dirname(__file__), "logs", "test-log4j.log")
    )
    assert isinstance(result, Log4jTransformer), "Should resolve as log4j transformer"
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
    # Hard to confidently resolve XML for Window events as of now
    with raises(ValueError, match="transformer could not be determined"):
        trans.get_transformer(os.path.join(os.path.dirname(__file__), "logs", "test.xml"))
    with raises(ValueError, match="transformer could not be determined"):
        trans.get_transformer(os.path.join(os.path.dirname(__file__), "logs", "test-jlu.log"))


def test_transformer_factory_undetermined():
    trans = Transformer(
        [
            JsonTransformer(),
            SyslogTransformer(),
            Log4jTransformer(),
            NcsaTransformer(),
            SipTransformer(),
            CefTransformer(),
            XMLTransformer(),
        ]
    )
    with raises(ValueError, match="transformer could not be determined"):
        trans.get_transformer(os.path.join(os.path.dirname(__file__), "logs", "test-unk.log"))


def test_transformer_by_name():
    trans = Transformer(
        [
            JsonTransformer(),
            SyslogTransformer(),
            Log4jTransformer(),
            NcsaTransformer(),
            SipTransformer(),
            CefTransformer(),
            XMLTransformer(),
        ]
    )
    result = trans.get_transformer("xml")
    assert isinstance(result, XMLTransformer), "Should resolve as xml transformer"
    result = trans.get_transformer("sys")
    assert isinstance(result, SyslogTransformer), "Should resolve as syslog transformer"
    result = trans.get_transformer("json")
    assert isinstance(result, JsonTransformer), "Should resolve as json transformer"
    result = trans.get_transformer("cef")
    assert isinstance(result, CefTransformer), "Should resolve as cef transformer"
    result = trans.get_transformer("ncsa")
    assert isinstance(result, NcsaTransformer), "Should resolve as ncsa transformer"
    result = trans.get_transformer("sip")
    assert isinstance(result, SipTransformer), "Should resolve as sip transformer"
    result = trans.get_transformer("log4j")
    assert isinstance(result, Log4jTransformer), "Should resolve as log4j transformer"
