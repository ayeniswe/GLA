from gla.analyzer.iterator import Unstructured
from gla.plugins.transformer.syslog_transformer import SyslogTransformer


def test_syslog_transformation(get_log_path):
    # ARRANGE
    syslog = SyslogTransformer()
    cases = [
        {
            "actual": "2025-07-20T17:41:00 NOTICE [example.com] example - This is a test message",
        },
        # Not correct strategy
        {
            "actual": None,
        },
        {
            "actual": "2025-07-21T17:41:00 NOTICE [myserver] myapp - Critical failure occurred",
        },
        {
            "actual": "2025-09-10T12:30:45 NOTICE [myserver] app1 - "
            "Failed login attempt from 192.168.0.1",
        },
        {
            "actual": "2025-05-15T09:20:00 ERROR [server1] myservice - "
            "User logged in successfully",
        },
        {
            "actual": "2025-04-02T10:15:00 INFO [appserver] app2 - Database connection lost",
        },
        {
            "actual": "2025-08-23T14:55:30 ALERT [testserver] testapp - Disk space running low",
        },
        {
            "actual": "2025-03-05T16:25:00 CRITICAL [prodserver] backup - "
            "Backup process completed",
        },
        {
            "actual": "2025-04-18T10:30:25 ERROR [webserver] webapp - User session expired",
        },
        # Not correct strategy
        {
            "actual": None,
        },
        {
            "actual": "2025-06-01T08:55:00 NOTICE [notaserver] testapp - "
            "Unexpected error occurred",
        },
        {
            "actual": "2025-02-28T14:25:00 EMERGENCY [another-server] anotherapp - "
            "File upload failed",
        },
        {
            "actual": "2025-09-11T13:00:00 WARN [myserver] myservice - File not found",
        },
        {
            "actual": "2025-01-10T18:20:00 ERROR [server3] app4 - Memory usage high",
        },
        {
            "actual": "2025-10-05T21:10:00 ERROR [clientserver] clientapp - Connection timeout",
        },
        {
            "actual": "2025-12-25T20:00:00 ALERT [loggingserver] logapp - Log rotation complete",
        },
        {
            "actual": "2025-05-05T23:59:00 DEBUG [mainserver] myservice - "
            "Service unavailable",
        },        
        {
            "actual": None,
        },
        {
            "actual": None,
        },
    ]
    iterator = Unstructured(get_log_path("test-syslog.log"), "utf-8", "\n")
    # Select correct strategy
    syslog.resolve((get_log_path("test-syslog.log"), "utf-8"))

    for idx, entry in enumerate(iterator):
        # ACT
        result = syslog.transform(entry)
        result = str(result) if result else result

        # ASSERT
        actual = cases[idx]["actual"]
        assert (result == actual), f"Failed for input: {entry}, expected: {actual}, Got: {result}"
