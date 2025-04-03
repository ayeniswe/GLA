import os

from pytest import raises

from gla.plugins.transformer.cef_transformer import CefTransformer
from gla.plugins.transformer.json_transformer import JsonTransformer
from gla.plugins.transformer.log4j_transformer import Log4jTransformer
from gla.plugins.transformer.ncsa_transformer import NcsaTransformer
from gla.plugins.transformer.sip_transformer import SipTransformer
from gla.plugins.transformer.syslog_transformer import SyslogTransformer
from gla.plugins.transformer.transformer import Transformer
from gla.plugins.transformer.xml_transformer import XMLTransformer


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
        os.path.join(os.path.dirname(__file__), "logs", "test-log4j.log"), encoding="utf-8"
    )
    assert isinstance(result, Log4jTransformer), "Should resolve as log4j transformer"
    result = trans.get_transformer(
        os.path.join(os.path.dirname(__file__), "logs", "test-syslog.log"), encoding="utf-8"
    )
    assert isinstance(result, SyslogTransformer), "Should resolve as syslog transformer"
    result = trans.get_transformer(
        os.path.join(os.path.dirname(__file__), "logs", "test-sip.log"), encoding="utf-8"
    )
    assert isinstance(result, SipTransformer), "Should resolve as sip transformer"
    result = trans.get_transformer(
        os.path.join(os.path.dirname(__file__), "logs", "test-ncsa.log"), encoding="utf-8"
    )
    assert isinstance(result, NcsaTransformer), "Should resolve as ncsa transformer"
    result = trans.get_transformer(
        os.path.join(os.path.dirname(__file__), "logs", "test-cef.log"), encoding="utf-8"
    )
    assert isinstance(result, CefTransformer), "Should resolve as cef transformer"
    # Hard to confidently resolve XML for Window events as of now
    with raises(ValueError, match="transformer could not be determined"):
        trans.get_transformer(
            os.path.join(os.path.dirname(__file__), "logs", "test.xml"), encoding="utf-16"
        )
    with raises(ValueError, match="transformer could not be determined"):
        trans.get_transformer(
            os.path.join(os.path.dirname(__file__), "logs", "test-jlu.log"), encoding="utf-8"
        )


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
