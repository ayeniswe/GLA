import os
from lxml.etree import iterparse, fromstring, Element
from gla.analyzer.iterator import Mode
from gla.plugins.transformer.xml_transformer import JLU, XMLTransformer
from gla.plugins.transformer.xmlfragment_transformer import WinEvent, XMLFragmentTransformer

# SETUP
def get_log_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), "logs", filename)

def test_xml_fragment_transformer_windows_events_strategy_transform_fails():
    strategy = WinEvent()
    # Strategy should not perform transformation
    assert strategy.do_action(Element("test")) is None

def test_xml_fragment_transformer_transforms_messages():
    transformer = XMLFragmentTransformer()

    # Resolve the transformer first to get correct strategy for transformation
    log_path = get_log_path("test.xml")
    transformer.resolve((log_path, "utf-16-le"))

    buffer = ""
    with open(log_path, "r", encoding="utf-16-le") as f:
        for line in f:
            buffer += line
            if line.strip() == "</Event>":
                try:
                    elem = fromstring(buffer)
                    res = transformer.transform(elem)
                    if res:
                        # Every transformation should process without error
                        assert res.message != ""
                finally:
                    buffer = ""

def test_xml_fragment_transformer_passed_validation():
    transformer = XMLFragmentTransformer()
    valid_file = get_log_path("test.xml")
    result = transformer.validate({
        "data": valid_file,
        "encoding": "utf-16"
    })
    # Strategy should auto-resolve after validation checks
    assert transformer._cache_strategy is not None
    # Validation checks should pass
    assert result is True

def test_xml_fragment_transformer_failed_validation():
    transformer = XMLFragmentTransformer()
    invalid_file = get_log_path("test-unk.log")
    result = transformer.validate({
        "data": invalid_file,
        "encoding": "utf-8"
    })
    # Strategy should fail auto-resolve after validation checks
    assert transformer._cache_strategy is None
    # Validation checks should pass
    assert result is False

def test_xml_transformer_transforms_messages():
    transformer = XMLTransformer()

    # Resolve the transformer first to get correct strategy for transformation
    log_path = get_log_path("test-jlu.log")
    transformer.resolve((log_path, "utf-8"))

    for event, elem in iterparse(log_path):
        res = transformer.transform(elem)
        if res:
            # Every transformation should process without error
            assert res.message != ""

def test_xml_transformer_failed_validation():
    transformer = XMLTransformer()
    invalid_file = get_log_path("test-unk.log")
    result = transformer.validate({
        "data": invalid_file,
        "encoding": "utf-8"
    })
    # Strategy should fail auto-resolve after validation checks
    assert transformer._cache_strategy is None
    # Validation checks should pass
    assert result is False

def test_xml_transformer_passed_validation():
    transformer = XMLTransformer()
    valid_file = get_log_path("test-jlu.log")
    result = transformer.validate({
        "data": valid_file,
        "encoding": "utf-8"
    })
    # Strategy should auto-resolve after validation checks
    assert transformer._cache_strategy is not None
    # Validation checks should pass
    assert result is True

def test_xml_transformer_is_structured():
    transformer = XMLTransformer()
    # Strategy should be of mode XML always
    assert transformer.mode == Mode.XML

def test_xml_transformer_java_util_logging_strategy_fails_to_resolve():
    strategy = JLU()
    log_path = get_log_path("test-jlu-extra.log")
    # Strategy should go too deep and fail
    assert strategy.score((log_path, "utf-8")) is False
