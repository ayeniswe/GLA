import dateparser
import re
from datetime import datetime
from log import Log
from plugins.transformer.transformer import (
    DIVIDER_RE,
    LEVEL_RE,
    MODULE_RE,
    MSG_RE,
    SOURCE_RE,
    TIME_RE,
    Transformer,
)


class CustomTransformer(Transformer):
    def transform(line: str):
        match = re.match(
            rf"{TIME_RE} {LEVEL_RE} {SOURCE_RE} {MODULE_RE} {DIVIDER_RE} {MSG_RE}",
            line,
        )
        if match:
            return Log(
                level=match["lvl"],
                module=match["mod"],
                source=match["src"],
                timestamp=dateparser.parse(match["time"]),
                message=match["msg"],
            )
        else:
            return None


def test_time_regex():
    assert (
        CustomTransformer.transform(
            "2020$01$01 12_34-56 ERROR class.example [main] - Error message goes here"
        )
        is None
    ), "Expected to fail and not process abritrary separators"

    assert CustomTransformer.transform(
        "2020-01-01T12:34:56 ERROR class.example [main] - Error message goes here"
    ) == Log(
        "ERROR",
        "main",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56", "%Y-%m-%d %H:%M:%S"),
        "class.example",
    ), "Expected to process datetime even if they have a 'T' in the middle"

    assert CustomTransformer.transform(
        "01-01-2024 12:34:56 ERROR class.example [main] - Error message goes here"
    ) == Log(
        "ERROR",
        "main",
        "Error message goes here",
        datetime.strptime("01-01-2024 12:34:56", "%m-%d-%Y %H:%M:%S"),
        "class.example",
    ), "Expected to process datetime even if organized by month-day-year"

    assert CustomTransformer.transform(
        "01-2024-01 12:34:56 ERROR class.example [main] - Error message goes here"
    ) == Log(
        "ERROR",
        "main",
        "Error message goes here",
        datetime.strptime("01-2024-01 12:34:56", "%m-%Y-%d %H:%M:%S"),
        "class.example",
    ), "Expected to process datetime even if organized by month-year-day"

    assert CustomTransformer.transform(
        "2020-01-01 12:34:56 ERROR class.example [main] - Error message goes here"
    ) == Log(
        "ERROR",
        "main",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56", "%Y-%m-%d %H:%M:%S"),
        "class.example",
    ), "Expected to process time even if milliseconds dont exist"

    assert CustomTransformer.transform(
        "2020-01-01 12:34:56.789 ERROR class.example [main] - Error message goes here"
    ) == Log(
        "ERROR",
        "main",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56.789", "%Y-%m-%d %H:%M:%S.%f"),
        "class.example",
    ), "Expected to process time even if milliseconds do exist"

    assert CustomTransformer.transform(
        "2020-01-01 ERROR class.example [main] - Error message goes here"
    ) == Log(
        "ERROR",
        "main",
        "Error message goes here",
        datetime.strptime("2020-01-01", "%Y-%m-%d"),
        "class.example",
    ), "Expected to process datetime even if clock time does not exist"

    assert CustomTransformer.transform(
        "12:34:56 ERROR class.example [main] - Error message goes here"
    ) == Log(
        "ERROR",
        "main",
        "Error message goes here",
        dateparser.parse("12:34:56"),
        "class.example",
    ), "Expected to process datetime even if date does not exist"


def test_level_regex():
    assert CustomTransformer.transform(
        "2020-01-01 12:34:56 [ERROR] class.example [main] - Error message goes here"
    ) == Log(
        "ERROR",
        "main",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56", "%Y-%m-%d %H:%M:%S"),
        "class.example",
    ), "Expected to ignore wrapping of level and still process"


def test_source_and_module_regex():
    assert CustomTransformer.transform(
        "2020-01-01 12:34:56 [ERROR] -class.example- -main- - Error message goes here"
    ) == Log(
        "ERROR",
        "main",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56", "%Y-%m-%d %H:%M:%S"),
        "class.example",
    ), "Expected to ignore wrapping of source or module and still process"

    assert CustomTransformer.transform(
        "2020-01-01 12:34:56 [ERROR] class$example.one main$class - Error message goes here"
    ) == Log(
        "ERROR",
        "main$class",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56", "%Y-%m-%d %H:%M:%S"),
        "class$example.one",
    ), "Expected to accept characters: [$.]"

    result: Log = CustomTransformer.transform(
        "2020-01-01 12:34:56 [ERROR] class-example main-class - Error message goes here"
    )
    assert (
        result is None
    ), f"Expected to not accept characters other than: [$.], but got {result.get_source()} and {result.get_module()}"
