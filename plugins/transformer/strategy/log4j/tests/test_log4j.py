from datetime import datetime
from log import Log
from plugins.transformer import TLSMM, TSLMM, LSMM, LM, LTSMM


def test_ltsmm():
    assert LTSMM.transform(
        "ERROR 2020-01-01 12:34:56.789 [main] class.example - Error message goes here"
    ) == Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56.789", "%Y-%m-%d %H:%M:%S.%f"),
        "main",
    ), "Expected Level Timestamp Source Module Message order to be processed"
    assert (
        LTSMM.transform(
            "2020-01-01 12:34:56.789 ERROR [main] class.example - Error message goes here"
        )
        is None
    ), "Expected Level Timestamp Source Module Message order to not be processed"


def test_tlsmm():
    assert TLSMM.transform(
        "2020-01-01 12:34:56.789 ERROR [main] class.example - Error message goes here"
    ) == Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56.789", "%Y-%m-%d %H:%M:%S.%f"),
        "main",
    ), "Expected Timestamp Level Source Module Message order to be processed"
    assert TLSMM.transform(
        "2020-01-01 12:34:56.789 ERROR class.example [main] - Error message goes here"
    ) != Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56.789", "%Y-%m-%d %H:%M:%S.%f"),
        "main",
    ), "Expected Timestamp Level Source Module Message order to not be processed"


def test_tslmm():
    assert TSLMM.transform(
        "2020-01-01 12:34:56.789 [main] ERROR class.example - Error message goes here"
    ) == Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56.789", "%Y-%m-%d %H:%M:%S.%f"),
        "main",
    ), "Expected Timestamp Source Level Module Message order to be processed"
    assert TSLMM.transform(
        "2020-01-01 12:34:56.789 ERROR [main] class.example - Error message goes here"
    ) != Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56.789", "%Y-%m-%d %H:%M:%S.%f"),
        "main",
    ), "Expected Timestamp Source Level Module Message to not process source and module correctly"


def test_lsmm():
    assert LSMM.transform(
        "ERROR [main] class.example - Error message goes here"
    ) == Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        source="main",
    ), "Expected Level Source Module Message to be processed"
    assert LSMM.transform(
        "ERROR class.example [main] - Error message goes here"
    ) != Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        source="main",
    ), "Expected Level Source Module Message to not process source and module correctly"
    assert (
        LSMM.transform("[main] ERROR class.example - Error message goes here") is None
    ), "Expected Level Source Module Message to not be processed"
    assert (
        LSMM.transform("[main] class.example ERROR - Error message goes here") is None
    ), "Expected Level Source Module Message to not be processed"
    assert (
        LSMM.transform("[main] class.example Error message goes here ERROR") is None
    ), "Expected Level Source Module Message to not be processed"


def test_lm():
    assert LM.transform("ERROR - message goes here") == Log(
        "ERROR",
        message="message goes here",
    ), "Expected Level  Message to be processed"
    assert (
        LM.transform("message goes here - ERROR") is None
    ), "Expected Level Message to not be processed"
