from gla.analyzer.iterator import Unstructured
from gla.plugins.transformer.log4j_transformer import Log4jTransformer


def test_log4j_transformation(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-02-01T00:00:00 WARN [worker-thread] database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-02-01T00:00:00 ERROR [main-thread] user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG [api-thread] api.controller - Fetching user data",
        },
        {
            "expected": "2020-01-02T00:00:00 INFO [network-thread] network.service - Server started successfully",
        },
        {
            "expected": "2021-05-06T00:00:00 ERROR [io-thread] file.io - Error reading file",
        },
        {
            "expected": "2021-07-08T00:00:00 WARN [worker-thread] user.profile - Missing profile information",
        },
        {
            "expected": "2020-09-10T00:00:00 DEBUG [api-thread] api.controller - Creating new user",
        },
        {
            "expected": "2020-02-01T00:00:00 ERROR server - Connection timeout",
        },
        {
            "expected": "2021-03-11T00:00:00 INFO [main] application - System is healthy",
        },
        {
            "expected": "2022-10-02T00:00:00 ERROR file.transfer - File not found",
        },
        {
            "expected": "2020-03-01T00:00:00 WARN [logging-thread] logger.service - Log rotation failed",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR [database-thread] db.query - SQL syntax error",
        },
        {
            "expected": "2020-01-02T00:00:00 ERROR [main-thread] db.connect - Failed to connect to database",
        },
        {
            "expected": "2021-09-10T00:00:00 ERROR [network-thread] api.request - Timeout error",
        },
        {
            "expected": "2021-11-11T00:00:00 ERROR [network-thread] api.request - Timeout error occurred",
        },
        {
            "expected": "2022-12-05T00:00:00 WARN [logging-thread] logger.service - Missing log file",
        },
        {
            "expected": None,
        },
        {
            "expected": None,
        },
        {
            "expected": "2020-03-05T00:00:00 ERROR user.auth - Invalid session",
        },
        {
            "expected": "2021-01-01T00:00:00 ERROR [api-thread] network.connect - Timeout",
        },
        {
            "expected": "2022-08-15T00:00:00 ERROR api.auth - Unauthorized access",
        },
    ]
    path = get_log_path("test-log4j.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    # check_transformer_test_cases(cases, iterator, log4j)
    for idx, entry in enumerate(iterator):
        # ACT
        result = log4j.transform(entry)
        result = str(result) if result else result

        # ASSERT
        try:
            actual = cases[idx]["expected"]
        except KeyError:
            raise KeyError("Every expected case must have a single key named 'expected'")
        except IndexError:
            raise IndexError("An expected case must be specified for each iteration of tests")
        assert (result == actual)

