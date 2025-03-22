from plugins.transformer.log4j_transformer import Log4jTransformer


def test_log4j_transformation():
    log4j = Log4jTransformer()

    test_cases = [
        {
            "input": "2020-02-01 [worker-thread] WARN "
            "database.connection - Failed to connect to database",
            "expected": "2020-02-01T00:00:00 WARN [worker-thread] database.connection - "
            "Failed to connect to database",
        },
        {
            "input": "02-2020-01 [main-thread] ERROR user.auth - Invalid login credentials",
            "expected": "2020-02-01T00:00:00 ERROR [main-thread] "
            "user.auth - Invalid login credentials",
        },
        {
            "input": "03-01-2020 [api-thread] DEBUG api.controller - Fetching user data",
            "expected": "2020-03-01T00:00:00 DEBUG [api-thread] "
            "api.controller - Fetching user data",
        },
        {
            "input": "2020-01-02 [network-thread] INFO network.service - "
            "Server started successfully",
            "expected": "2020-01-02T00:00:00 INFO [network-thread] "
            "network.service - Server started successfully",
        },
        {
            "input": "2021-05-06 [io-thread] ERROR file.io - Error reading file",
            "expected": "2021-05-06T00:00:00 ERROR [io-thread] file.io - Error reading file",
        },
        {
            "input": "2021-07-08 [worker-thread] WARN user.profile - Missing profile information",
            "expected": "2021-07-08T00:00:00 WARN [worker-thread] user.profile - "
            "Missing profile information",
        },
        {
            "input": "2020-09-10 [api-thread] DEBUG api.controller - Creating new user",
            "expected": "2020-09-10T00:00:00 DEBUG [api-thread] api.controller - "
            "Creating new user",
        },
        {
            "input": "02-01-2020 ERROR server - Connection timeout",
            "expected": "2020-02-01T00:00:00 ERROR server - Connection timeout",
        },
        {
            "input": "2021-03-11 [main] INFO application - System is healthy",
            "expected": "2021-03-11T00:00:00 INFO [main] application - System is healthy",
        },
        {
            "input": "2022-10-02 ERROR file.transfer - File not found",
            "expected": "2022-10-02T00:00:00 ERROR file.transfer - File not found",
        },
        {
            "input": "03-01-2020 [logging-thread] WARN logger.service - Log rotation failed",
            "expected": "2020-03-01T00:00:00 WARN [logging-thread] logger.service - "
            "Log rotation failed",
        },
        {
            "input": "03-01-2020 ERROR [database-thread] db.query - SQL syntax error",
            "expected": "2020-03-01T00:00:00 ERROR [database-thread] db.query - SQL syntax error",
        },
        {
            "input": "[main-thread] 2020-01-02 ERROR db.connect - Failed to connect to database",
            "expected": "2020-01-02T00:00:00 ERROR [main-thread] db.connect - "
            "Failed to connect to database",
        },
        {
            "input": "ERROR [network-thread] api.request - Timeout error 2021-09-10",
            "expected": "2021-09-10T00:00:00 ERROR [network-thread] api.request - Timeout error",
        },
        {
            "input": "[network-thread] api.request ERROR 2021-11-11 - Timeout error occurred",
            "expected": "2021-11-11T00:00:00 ERROR [network-thread] api.request - "
            "Timeout error occurred",
        },
        {
            "input": "[logging-thread] WARN logger.service 2022-12-05 - Missing log file",
            "expected": "2022-12-05T00:00:00 WARN [logging-thread] logger.service - "
            "Missing log file",
        },
        {
            "input": "class.example Error message goes here 02-01-2020 ERROR [main]",
            "expected": None,
        },
        {
            "input": "class.example Error message goes here ERROR 02-01-2020 [main]",
            "expected": None,
        },
        {
            "input": "2020-03-05 ERROR user.auth - Invalid session",
            "expected": "2020-03-05T00:00:00 ERROR user.auth - Invalid session",
        },
        {
            "input": "[api-thread] 2021-01-01 ERROR network.connect - Timeout",
            "expected": "2021-01-01T00:00:00 ERROR [api-thread] network.connect - Timeout",
        },
        {
            "input": "2022-08-15 ERROR api.auth - Unauthorized access",
            "expected": "2022-08-15T00:00:00 ERROR api.auth - Unauthorized access",
        },
    ]

    for case in test_cases:
        input_log = case["input"]
        expected_result = case["expected"]
        result = log4j._transform(input_log)
        if expected_result:
            assert (
                str(result) == expected_result
            ), f"Failed for input: {input_log}, Expected: {expected_result}, Got: {str(result)}"
        else:
            assert (
                result is None
            ), f"Failed for input: {input_log}, Expected: None, Got: {str(result)}"
