from gla.analyzer.iterator import Unstructured
from gla.plugins.transformer.log4j_transformer import Log4jTransformer


def test_log4j_transformation(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN [worker-thread] database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR [main-thread] user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG [api-thread] api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO [network-thread] network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation2(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN [worker-thread] database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR [main-thread] user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG [api-thread] api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO [network-thread] network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j2.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation3(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN [worker-thread] database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR [main-thread] user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG [api-thread] api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO [network-thread] network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j3.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation4(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN [worker-thread] database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR [main-thread] user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG [api-thread] api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO [network-thread] network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j4.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation5(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j5.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation6(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j6.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation6(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j6.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation6(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j6.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation7(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j7.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation6(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j6.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation6(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j6.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation6(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j6.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation6(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j6.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation6(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j6.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation6(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j6.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation6(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j6.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation6(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j6.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)


def test_log4j_transformation6(get_log_path, check_transformer_test_cases):
    # ARRANGE
    log4j = Log4jTransformer()
    cases = [
        {
            "expected": "2020-03-01T00:00:00 WARN database.connection - Failed to connect to database",
        },
        {
            "expected": "2020-03-01T00:00:00 ERROR user.auth - Invalid login credentials",
        },
        {
            "expected": "2020-03-01T00:00:00 DEBUG api.controller - Fetching user data",
        },
        {
            "expected": "2020-03-01T00:00:00 INFO network.service - Server started successfully",
        },
    ]
    path = get_log_path("test-log4j6.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    log4j.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, log4j)
