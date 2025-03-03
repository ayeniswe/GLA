from datetime import datetime
from log import Log
from plugins.transformer.log4j.log4j import (
    LVL_SRC_MOD_MSG,
    TIME_LVL_SRC_MOD_MSG,
    TIME_SRC_LVL_MOD_MSG,
    LVL_MSG,
    LVL_TIME_SRC_MOD_MSG,
)


def test_ltsmm():
    assert LVL_TIME_SRC_MOD_MSG.transform(
        "ERROR 2020-01-01 12:34:56.789 [main] class.example - Error message goes here"
    ) == Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56.789", "%Y-%m-%d %H:%M:%S.%f"),
        "main",
    ), "Expected Level Timestamp Source Module Message order to be processed"
    assert (
        LVL_TIME_SRC_MOD_MSG.transform(
            "2020-01-01 12:34:56.789 ERROR [main] class.example - Error message goes here"
        )
        is None
    ), "Expected Level Timestamp Source Module Message order to not be processed"


def test_tlsmm():
    assert TIME_LVL_SRC_MOD_MSG.transform(
        "2020-01-01 12:34:56.789 ERROR [main] class.example - Error message goes here"
    ) == Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56.789", "%Y-%m-%d %H:%M:%S.%f"),
        "main",
    ), "Expected Timestamp Level Source Module Message order to be processed"
    assert TIME_LVL_SRC_MOD_MSG.transform(
        "2020-01-01 12:34:56.789 ERROR class.example [main] - Error message goes here"
    ) != Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56.789", "%Y-%m-%d %H:%M:%S.%f"),
        "main",
    ), "Expected Timestamp Level Source Module Message order to not be processed"


def test_tslmm():
    assert TIME_SRC_LVL_MOD_MSG.transform(
        "2020-01-01 12:34:56.789 [main] ERROR class.example - Error message goes here"
    ) == Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56.789", "%Y-%m-%d %H:%M:%S.%f"),
        "main",
    ), "Expected Timestamp Source Level Module Message order to be processed"
    assert TIME_SRC_LVL_MOD_MSG.transform(
        "2020-01-01 12:34:56.789 ERROR [main] class.example - Error message goes here"
    ) != Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56.789", "%Y-%m-%d %H:%M:%S.%f"),
        "main",
    ), "Expected Timestamp Source Level Module Message to not process source and module correctly"


def test_lsmm():
    assert LVL_SRC_MOD_MSG.transform(
        "ERROR [main] class.example - Error message goes here"
    ) == Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        source="main",
    ), "Expected Level Source Module Message to be processed"
    assert LVL_SRC_MOD_MSG.transform(
        "ERROR class.example [main] - Error message goes here"
    ) != Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        source="main",
    ), "Expected Level Source Module Message to not process source and module correctly"
    assert (
        LVL_SRC_MOD_MSG.transform(
            "[main] ERROR class.example - Error message goes here"
        )
        is None
    ), "Expected Level Source Module Message to not be processed"
    assert (
        LVL_SRC_MOD_MSG.transform(
            "[main] class.example ERROR - Error message goes here"
        )
        is None
    ), "Expected Level Source Module Message to not be processed"
    assert (
        LVL_SRC_MOD_MSG.transform("[main] class.example Error message goes here ERROR")
        is None
    ), "Expected Level Source Module Message to not be processed"


def test_lm():
    assert LVL_MSG.transform("ERROR - message goes here") == Log(
        "ERROR",
        message="message goes here",
    ), "Expected Level  Message to be processed"
    assert (
        LVL_MSG.transform("message goes here - ERROR") is None
    ), "Expected Level Message to not be processed"
