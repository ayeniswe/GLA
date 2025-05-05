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
from gla.plugins.transformer.xmlfragment_transformer import XMLFragmentTransformer


def test_transformer_factory_by_path(get_log_path):
    # ARRANGE
    trans = Transformer(
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
    )

    # ACT
    result_log4j = trans.get_transformer(get_log_path("test-log4j.log"), encoding="utf-8")
    result_syslog = trans.get_transformer(get_log_path("test-syslog.log"), encoding="utf-8")
    result_sip = trans.get_transformer(get_log_path("test-sip.log"), encoding="utf-8")
    result_ncsa = trans.get_transformer(get_log_path("test-ncsa.log"), encoding="utf-8")
    result_cef = trans.get_transformer(get_log_path("test-cef.log"), encoding="utf-8")
    result_xmlfrag = trans.get_transformer(get_log_path("test.xml"), encoding="utf-16")
    result_xml = trans.get_transformer(get_log_path("test-jlu.log"), encoding="utf-8")

    # ASSERT
    assert isinstance(result_log4j, Log4jTransformer), "Should resolve as log4j transformer"
    assert isinstance(result_syslog, SyslogTransformer), "Should resolve as syslog transformer"
    assert isinstance(result_sip, SipTransformer), "Should resolve as sip transformer"
    assert isinstance(result_ncsa, NcsaTransformer), "Should resolve as ncsa transformer"
    assert isinstance(result_cef, CefTransformer), "Should resolve as cef transformer"
    assert isinstance(
        result_xmlfrag, XMLFragmentTransformer
    ), "Should resolve as xml fragment transformer"
    assert isinstance(result_xml, XMLTransformer), "Should resolve as xml transformer"


def test_transformer_factory_undetermined():
    # ARRANGE
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

    # ACT-ASSERT
    with raises(ValueError, match="transformer could not be determined"):
        trans.get_transformer(os.path.join(os.path.dirname(__file__), "logs", "test-unk.log"))
