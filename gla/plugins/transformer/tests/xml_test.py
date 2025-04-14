from lxml.etree import iterparse, fromstring, Element
from gla.analyzer.iterator import Mode
from gla.plugins.transformer.xml_transformer import JLU, XMLTransformer
from gla.plugins.transformer.xmlfragment_transformer import WinEvent, XMLFragmentTransformer

def test_xml_fragment_transformer_windows_events_strategy_transform_fails():
    # ARRANGE
    strategy = WinEvent()
    
    # ACT
    actual = strategy.do_action(Element("test"))

    # ASSERT
    # Strategy should not perform transformation
    assert actual is None

def test_xml_fragment_transformer_transforms_messages(get_log_path):
    # ARRANGE
    transformer = XMLFragmentTransformer()
    # Resolve the transformer first to get correct strategy for transformation
    log_path = get_log_path("test.xml")
    transformer.resolve((log_path, "utf-16-le"))

    # ACT
    buffer = ""
    missed_transform = False
    with open(log_path, "r", encoding="utf-16-le") as f:
        for line in f:
            buffer += line
            if line.strip() == "</Event>":
                try:
                    elem = fromstring(buffer)
                    res = transformer.transform(elem)
                    if not res:
                        missed_transform = True
                        break
                    if res.message == "":
                        missed_transform = True
                        break

                finally:
                    buffer = ""

    # ASSERT
    # Every transformation should process without error
    assert not missed_transform

def test_xml_fragment_transformer_passed_validation(get_log_path):
    # ARRANGE
    transformer = XMLFragmentTransformer()
    valid_file = get_log_path("test.xml")

    # ACT
    result = transformer.validate({
        "data": valid_file,
        "encoding": "utf-16"
    })

    # ASSERT
    # Strategy should auto-resolve after validation checks
    assert transformer._cache_strategy is not None
    # Validation checks should pass
    assert result is True

def test_xml_fragment_transformer_failed_validation(get_log_path):
    # ARRANGE
    transformer = XMLFragmentTransformer()
    invalid_file = get_log_path("test-unk.log")

    # ACT
    result = transformer.validate({
        "data": invalid_file,
        "encoding": "utf-8"
    })

    # ASSERT
    # Strategy should fail auto-resolve after validation checks
    assert transformer._cache_strategy is None
    # Validation checks should pass
    assert result is False

def test_xml_transformer_transforms_messages(get_log_path):
    # ARRANGE
    transformer = XMLTransformer()
    # Resolve the transformer first to get correct strategy for transformation
    log_path = get_log_path("test-jlu.log")
    transformer.resolve((log_path, "utf-8"))

    # ACT
    missed_transform = False
    for event, elem in iterparse(log_path):
        res = transformer.transform(elem)
        # Some tags may be ignore so transformed would failed
        if res and res.message == "":
            missed_transform = True
            break

    # ASSERT
    # Every transformation should process without error
    assert not missed_transform

def test_xml_transformer_failed_validation(get_log_path):
    # ARRANGE
    transformer = XMLTransformer()
    invalid_file = get_log_path("test-unk.log")
    
    # ACT
    result = transformer.validate({
        "data": invalid_file,
        "encoding": "utf-8"
    })

    # ASSERT
    # Strategy should fail auto-resolve after validation checks
    assert transformer._cache_strategy is None
    # Validation checks should pass
    assert result is False

def test_xml_transformer_passed_validation(get_log_path):
    # ARRANGE
    transformer = XMLTransformer()
    valid_file = get_log_path("test-jlu.log")

    # ACT
    result = transformer.validate({
        "data": valid_file,
        "encoding": "utf-8"
    })

    # ASSERT
    # Strategy should auto-resolve after validation checks
    assert transformer._cache_strategy is not None
    # Validation checks should pass
    assert result is True

def test_xml_transformer_is_structured():
    # ARRANGE
    
    # ACT
    transformer = XMLTransformer()
    
    # ASSERT
    # Strategy should be of mode XML always
    assert transformer.mode == Mode.XML

def test_xml_transformer_java_util_logging_strategy_fails_to_resolve(get_log_path):
    # ARRANGE
    strategy = JLU()
    log_path = get_log_path("test-jlu-extra.log")

    # ACT
    actual = strategy.score((log_path, "utf-8"))

    # ASSERT
    # Strategy should go too deep and fail
    assert not actual
