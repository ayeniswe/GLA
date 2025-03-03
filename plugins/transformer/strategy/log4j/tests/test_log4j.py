from datetime import datetime
from log import Log
from plugins.transformer import TLSMM, TSLMM, LSMM, LM


def test_tlsmm():
    assert TLSMM.transform(
        "2020-01-01 12:34:56.789 ERROR [main] class.example - Error message goes here"
    ) == Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56.789", "%Y-%m-%d %H:%M:%S.%f"),
        "main",
    )
    assert TLSMM.transform(
        "2020-01-01 12:34:56.789 ERROR class.example [main] - Error message goes here"
    ) != Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56.789", "%Y-%m-%d %H:%M:%S.%f"),
        "main",
    )


def test_tslmm():
    assert TSLMM.transform(
        "2020-01-01 12:34:56.789 [main] ERROR class.example - Error message goes here"
    ) == Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56.789", "%Y-%m-%d %H:%M:%S.%f"),
        "main",
    )
    assert TSLMM.transform(
        "2020-01-01 12:34:56.789 ERROR [main] class.example - Error message goes here"
    ) != Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        datetime.strptime("2020-01-01 12:34:56.789", "%Y-%m-%d %H:%M:%S.%f"),
        "main",
    )


def test_lsmm():
    assert LSMM.transform(
        "ERROR [main] class.example - Error message goes here"
    ) == Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        source="main",
    )
    assert (
        LSMM.transform("[main] ERROR class.example - Error message goes here") is None
    )
    assert (
        LSMM.transform("[main] class.example ERROR - Error message goes here") is None
    )
    assert LSMM.transform("[main] class.example Error message goes here ERROR") is None


def test_lm():
    assert LM.transform("ERROR - message goes here") == Log(
        "ERROR",
        message="message goes here",
    )
    assert LM.transform("message goes here - ERROR") is None
