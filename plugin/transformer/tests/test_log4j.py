from plugin.transformer import Log4jTransformer


def test_log4j_transformation():
    log4j = Log4jTransformer()

    test_cases = [
        ("2020-02-01 [main] ERROR class.example - Error message goes here", True),
        ("02-2020-01 [main] ERROR class.example - Error message goes here", True),
        ("02-01-2020 [main] ERROR class.example - Error message goes here", True),
        ("02-01-2020 ERROR [main] class.example - Error message goes here", True),
        ("02-01-2020 ERROR class.example [main] - Error message goes here", True),
        ("02-01-2020 ERROR class.example Error message goes here [main]", True),
        ("02-01-2020 class.example ERROR Error message goes here [main]", True),
        ("02-01-2020 class.example Error message goes here ERROR [main]", True),
        ("02-01-2020 class.example Error message goes here [main] ERROR", True),
        ("[main] 02-01-2020 ERROR class.example - Error message goes here", True),
        ("[main] ERROR 02-01-2020 class.example - Error message goes here", True),
        ("[main] ERROR class.example 02-01-2020 - Error message goes here", False),
        ("[main] ERROR class.example Error message goes here 02-01-2020", True),
        ("ERROR [main] class.example Error message goes here 02-01-2020", True),
        ("ERROR class.example [main] Error message goes here 02-01-2020", True),
        ("ERROR class.example Error message goes here [main] 02-01-2020", True),
        ("ERROR class.example Error message goes here 02-01-2020 [main]", True),
        ("class.example 02-01-2020 Error message goes here [main] ERROR", True),
        ("class.example 02-01-2020 [main] Error message goes here ERROR", True),
        ("class.example 02-01-2020 [main] ERROR - Error message goes here", True),
        ("class.example [main] 02-01-2020 ERROR - Error message goes here", True),
        ("class.example [main] ERROR 02-01-2020 - Error message goes here", True),
        ("class.example [main] ERROR Error message goes here 02-01-2020", True),
        ("class.example ERROR [main] Error message goes here 02-01-2020", True),
        ("class.example ERROR Error message goes here [main] 02-01-2020", True),
        ("class.example ERROR Error message goes here 02-01-2020 [main]", True),
        ("class.example Error message goes here ERROR 02-01-2020 [main]", False),
        ("class.example Error message goes here 02-01-2020 ERROR [main]", True),
        ("class.example Error message goes here 02-01-2020 [main] ERROR", True),
    ]

    for test in test_cases:
        (log, should_be) = test
        result = log4j.transform(log)
        if should_be:
            assert (
                str(result)
                == "2020-02-01T00:00:00 ERROR [main] class.example - Error message goes here"
            )
        else:
            assert result == None
