import os

from pytest import raises

from plugins.transformer import Transformer
from plugins.transformer.json_transformer import JsonTransformer
from plugins.transformer.log4j_transformer import Log4jTransformer
from plugins.transformer.syslog_transformer import SyslogTransformer
from plugins.transformer.xml_transformer import XMLTransformer


def test_transformer_factory():
    trans = Transformer(
        [
            JsonTransformer(),
            SyslogTransformer(),
            Log4jTransformer(),
            XMLTransformer(),
        ]
    )
    trans = trans.get_transformer(os.path.join(os.path.dirname(__file__), "logs", "test-log4j.log"))
    assert isinstance(trans, Log4jTransformer), "Should resolve as log4j transformer"


def test_transformer_factory_undetermined():
    trans = Transformer(
        [
            JsonTransformer(),
            SyslogTransformer(),
            Log4jTransformer(),
            XMLTransformer(),
        ]
    )
    with raises(ValueError, match="transformer could not be determined"):
        trans.get_transformer(os.path.join(os.path.dirname(__file__), "logs", "test-unk.log"))
