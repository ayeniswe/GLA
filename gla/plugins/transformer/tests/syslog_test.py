from gla.analyzer.iterator import Unstructured
from gla.plugins.transformer.syslog_transformer import SyslogTransformer


def test_syslog_transformation(get_log_path, check_transformer_test_cases):
    # ARRANGE
    syslog = SyslogTransformer()
    cases = [
        {
            "expected": "2025-07-20T17:41:00 NOTICE [example.com] example - This is a test message",
        },
        # Not correct strategy
        {
            "expected": None,
        },
        {
            "expected": "2025-07-21T17:41:00 NOTICE [myserver] myapp - Critical failure occurred",
        },
        {
            "expected": "2025-09-10T12:30:45 NOTICE [myserver] app1 - "
            "Failed login attempt from 192.168.0.1",
        },
        {
            "expected": "2025-05-15T09:20:00 ERROR [server1] myservice - "
            "User logged in successfully",
        },
        {
            "expected": "2025-04-02T10:15:00 INFO [appserver] app2 - Database connection lost",
        },
        {
            "expected": "2025-08-23T14:55:30 ALERT [testserver] testapp - Disk space running low",
        },
        {
            "expected": "2025-03-05T16:25:00 CRITICAL [prodserver] backup - "
            "Backup process completed",
        },
        {
            "expected": "2025-04-18T10:30:25 ERROR [webserver] webapp - User session expired",
        },
        # Not correct strategy
        {
            "expected": None,
        },
        {
            "expected": "2025-06-01T08:55:00 NOTICE [notaserver] testapp - "
            "Unexpected error occurred",
        },
        {
            "expected": "2025-02-28T14:25:00 EMERGENCY [another-server] anotherapp - "
            "File upload failed",
        },
        {
            "expected": "2025-09-11T13:00:00 WARN [myserver] myservice - File not found",
        },
        {
            "expected": "2025-01-10T18:20:00 ERROR [server3] app4 - Memory usage high",
        },
        {
            "expected": "2025-10-05T21:10:00 ERROR [clientserver] clientapp - Connection timeout",
        },
        {
            "expected": "2025-12-25T20:00:00 ALERT [loggingserver] logapp - Log rotation complete",
        },
        {
            "expected": "2025-05-05T23:59:00 DEBUG [mainserver] myservice - "
            "Service unavailable",
        },        
        {
            "expected": None,
        },
        {
            "expected": None,
        },
    ]
    path = get_log_path("test-syslog.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    syslog.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, syslog)
