from plugins.transformer.log4j.log4j import (
    LVL_MSG,
    LVL_SRC_MOD_MSG,
    LVL_TIME_SRC_MOD_MSG,
    TIME_LVL_SRC_MOD_MSG,
    TIME_SRC_LVL_MOD_MSG,
)
from plugins.transformer.management import Management


def test_log_format_resolve():
    management = Management(
        [
            TIME_SRC_LVL_MOD_MSG,
            TIME_LVL_SRC_MOD_MSG,
            LVL_TIME_SRC_MOD_MSG,
            LVL_SRC_MOD_MSG,
            LVL_MSG,
        ]
    )
    assert (
        management.resolve(
            "ERROR 2020-01-01 12:34:56.789 [main] class.example - Error message goes here"
        )
        == LVL_TIME_SRC_MOD_MSG
    ), "Expected to resolve with the LVL_TIME_SRC_MOD_MSG strategy"
    assert (
        management.resolve(
            "2020-01-01 12:34:56.789 [main] ERROR class.example - Error message goes here"
        )
        == TIME_SRC_LVL_MOD_MSG
    ), "Expected to resolve with the TIME_SRC_LVL_MOD_MSG strategy"
    assert (
        management.resolve(
            "2020-01-01 12:34:56.789 ERROR [main] class.example - Error message goes here"
        )
        == TIME_LVL_SRC_MOD_MSG
    ), "Expected to resolve with the TIME_LVL_SRC_MOD_MSG strategy"
    assert (
        management.resolve("ERROR [main] class.example - Error message goes here")
        == LVL_SRC_MOD_MSG
    ), "Expected to resolve with the LVL_SRC_MOD_MSG strategy"
    assert (
        management.resolve("ERROR - message goes here") == LVL_MSG
    ), "Expected to resolve with the LVL_MSG strategy"
