from gla.plugins.transformer.syslog_transformer import SyslogTransformer


def test_syslog_transformation():
    syslog = SyslogTransformer()

    test_cases = [
        {
            "input": "<34>1 2003-10-11T22:14:15.000003+04:00 192.18.0.9 su 67 ID47 "
            '[exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"][poooo] '
            "'su root' failed for lonvick on /dev/pts/8",
            "expected": "2003-10-11T22:14:15.000003+04:00 CRITICAL [192.18.0.9] su - "
            "'su root' failed for lonvick on /dev/pts/8",
        },
        {
            "input": "<165>Jul 20 17:41:00 example.com example: This is a test message",
            "expected": "2025-07-20T17:41:00 NOTICE [example.com] example - This is a test message",
        },
        {
            "input": "<165>Jul 21 17:41:00 myserver myapp: Critical failure occurred",
            "expected": "2025-07-21T17:41:00 NOTICE [myserver] myapp - Critical failure occurred",
        },
        {
            "input": "<101>Sep 10 12:30:45 myserver app1: " "Failed login attempt from 192.168.0.1",
            "expected": "2025-09-10T12:30:45 NOTICE [myserver] app1 - "
            "Failed login attempt from 192.168.0.1",
        },
        {
            "input": "<99>May 15 09:20:00 server1 myservice: User logged in successfully",
            "expected": "2025-05-15T09:20:00 ERROR [server1] myservice - "
            "User logged in successfully",
        },
        {
            "input": "<110>Apr 2 10:15:00 appserver app2: Database connection lost",
            "expected": "2025-04-02T10:15:00 INFO [appserver] app2 - Database connection lost",
        },
        {
            "input": "<65>Aug 23 14:55:30 testserver testapp: Disk space running low",
            "expected": "2025-08-23T14:55:30 ALERT [testserver] testapp - Disk space running low",
        },
        {
            "input": "<74>Mar 5 16:25:00 prodserver backup: Backup process completed",
            "expected": "2025-03-05T16:25:00 CRITICAL [prodserver] backup - "
            "Backup process completed",
        },
        {
            "input": """<99>Apr 18 10:30:25 webserver webapp: User session expired""",
            "expected": "2025-04-18T10:30:25 ERROR [webserver] webapp - User session expired",
        },
        {
            "input": "<34>1 2021-01-01T00:00:00+00:00 192.168.0.100 systemd 12 ID123 "
            "[sdid@12345 eventSource='system' eventID='1001'][login] User 'root' logged in",
            "expected": "2021-01-01T00:00:00+00:00 CRITICAL [192.168.0.100] systemd - "
            "User 'root' logged in",
        },
        {
            "input": """<165>Jun 1 08:55:00 notaserver testapp: Unexpected error occurred""",
            "expected": "2025-06-01T08:55:00 NOTICE [notaserver] testapp - "
            "Unexpected error occurred",
        },
        {
            "input": """<32>Feb 28 14:25:00 another-server anotherapp: File upload failed""",
            "expected": "2025-02-28T14:25:00 EMERGENCY [another-server] anotherapp - "
            "File upload failed",
        },
        {
            "input": "<300>Sep 11 13:00:00 myserver myservice: File not found",
            "expected": "2025-09-11T13:00:00 WARN [myserver] myservice - File not found",
        },
        {
            "input": "<51>Jan 10 18:20:00 server3 app4: Memory usage high",
            "expected": "2025-01-10T18:20:00 ERROR [server3] app4 - Memory usage high",
        },
        {
            "input": "<123>Oct 5 21:10:00 clientserver clientapp: Connection timeout",
            "expected": "2025-10-05T21:10:00 ERROR [clientserver] clientapp - Connection timeout",
        },
        {
            "input": "<145>Dec 25 20:00:00 loggingserver logapp: Log rotation complete",
            "expected": "2025-12-25T20:00:00 ALERT [loggingserver] logapp - Log rotation complete",
        },
        {
            "input": "<34>May 5 23:59:00 mainserver myservice: Service unavailable",
            "expected": "2025-05-05T23:59:00 CRITICAL [mainserver] myservice - "
            "Service unavailable",
        },
        # Invalid log entry
        {
            "input": """<100>Invalid message format with missing timestamp and severity""",
            "expected": None,
        },
        # Invalid log entry
        {
            "input": "Invalid message without proper format",
            "expected": None,
        },
    ]

    for case in test_cases:
        input_log = case["input"]
        expected_result = case["expected"]
        result = syslog.transform(input_log)

        if expected_result:
            assert (
                str(result) == expected_result
            ), f"Failed for input: {input_log}, Expected: {expected_result}, Got: {str(result)}"
        else:
            assert (
                result is None
            ), f"Failed for input: {input_log}, Expected: None, Got: {str(result)}"
