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


def test_lsmm():
    assert LSMM.transform(
        "ERROR [main] class.example - Error message goes here"
    ) == Log(
        "ERROR",
        "class.example",
        "Error message goes here",
        source="main",
    )


def test_lm():
    assert LM.transform("ERROR - Error message goes here") == Log(
        "ERROR",
        message="Error message goes here",
    )
