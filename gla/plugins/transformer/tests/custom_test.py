
import dateparser
from pytest import raises
from gla.constants import LANGUAGES_SUPPORTED
from gla.plugins.transformer.custom_transformer import CustomTransformer


def test_valid_transformation():
    template = [";", "time", "lvl", "src", "mod", "msg"]
    log_entry = "2024-05-09;WARNING;dump.py;mod;hello world"

    transformer = CustomTransformer(template)
    log = transformer.transform(log_entry)

    assert log.level == "WARNING"
    assert log.module == "mod"
    assert log.message == "hello world"
    assert log.timestamp == dateparser.parse("2024-05-09", languages=LANGUAGES_SUPPORTED)
    assert log.source == "dump.py"


def test_invalid_template_length():
    with raises(ValueError, match="missing atleast 'one' gla log header"):
        CustomTransformer([";"])  # Only delimiter provided


def test_invalid_log_header():
    with raises(ValueError, match="'invalid' is not a valid gla log header"):
        CustomTransformer([";", "time", "lvl", "invalid"])


def test_mismatched_entry_and_template():
    template = [";", "time", "lvl", "msg"]
    log_entry = "2024-05-09;WARNING;hello world;extra_field"

    transformer = CustomTransformer(template)
    
    with raises(ValueError, match="template does not align with the log message"):
        transformer.transform(log_entry)


def test_extra_message_parts():
    template = [";", "time", "lvl", "msg"]
    log_entry = "2024-05-09;WARNING;this is a long message with extra words"

    transformer = CustomTransformer(template)
    log = transformer.transform(log_entry)

    assert log.message == "this is a long message with extra words"


def test_incorrect_delimiter():
    template = [",", "time", "lvl", "src", "mod", "msg"]
    log_entry = "2024-05-09;WARNING;dump.py;mod;hello world"  # Uses `;` instead of `,`

    transformer = CustomTransformer(template)

    with raises(ValueError, match="template does not align with the log message"):
        transformer.transform(log_entry)


def test_partial_log_message():
    template = [";", "time", "lvl", "msg"]
    log_entry = "2024-05-09;WARNING;"

    transformer = CustomTransformer(template)
    log = transformer.transform(log_entry)

    assert log.message is None


def test_empty_log_entry():
    template = [";", "time", "lvl", "msg"]
    log_entry = ""

    transformer = CustomTransformer(template)
    
    with raises(ValueError, match="template does not align with the log message"):
        transformer.transform(log_entry)


def test_null_values_in_log():
    template = [";", "time", "lvl", "src", "mod", "msg"]
    log_entry = ";;;;;"

    transformer = CustomTransformer(template)
    
    with raises(ValueError, match="\['time', 'lvl', 'src', 'mod', 'msg'\] template does not align with the log message: ;;;;;"):
        transformer.transform(log_entry)


def test_multiple_extensions():
    template = [";", "time", "lvl", "src", "mod", "msg", "ext", "ext"]
    log_entry = "2024-05-09;WARNING;dump.py;mod;hello;extra1;extra2"

    transformer = CustomTransformer(template)
    log = transformer.transform(log_entry)

    assert log.message == "hello extra1 extra2"
