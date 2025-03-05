from plugins.transformer import Log4jTransformer


def test_log4j_transformation():
    log4j = Log4jTransformer(
        [
            # Standard log4j format but diffrent orders
            r"^(?P<time>\d{4}-\d{2}-\d{2})\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
            r"^(?P<time>\d{2}-\d{4}-\d{2})\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
            r"^(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
            r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>\w+)\]\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
            r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]",
            r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+\[(?P<thread>\w+)\]\s+-\s+(?P<msg>.+)",
            r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]",
            r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>\w+)\]",
            r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
            r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
            r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
            r"^\[(?P<thread>\w+)\]\s+(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
            r"^\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
            r"^\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})",
            r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>\w+)\]\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})",
            r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+\[(?P<thread>\w+)\]\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})",
            r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<time>\d{2}-\d{2}-\d{4})",
            r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]",
            r"^(?P<mod>[\w.]+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
            r"^(?P<mod>[\w.]+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]\s+(?P<msg>.+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
            r"^(?P<mod>[\w.]+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+-\s+(?P<msg>.+)",
            r"^(?P<mod>[\w.]+)\s+\[(?P<thread>\w+)\]\s+(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+-\s+(?P<msg>.+)",
            r"^(?P<mod>[\w.]+)\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+-\s+(?P<msg>.+)",
            r"^(?P<mod>[\w.]+)\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})",
            r"^(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>\w+)\]\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})",
            r"^(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<time>\d{2}-\d{2}-\d{4})",
            r"^(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]",
            r"^(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>\w+)\]",
            r"^(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
        ]
    )

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
