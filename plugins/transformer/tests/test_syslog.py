from plugins.transformer.syslog_transformer import SyslogTransformer


def test_syslog():
    syslog = SyslogTransformer()
    assert (
        str(
            syslog.transform(
                """<34>1 2003-10-11T22:14:15.000003+04:00 192.18.0.9 su 67 ID47 [exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"][poooo] 'su root' failed for lonvick on /dev/pts/8"""
            )
        )
        == "2003-10-11T22:14:15.000003+04:00 CRITICAL [192.18.0.9] su - 'su root' failed for lonvick on /dev/pts/8"
    )
    assert (
        str(
            syslog.transform(
                "<165>Jul 20 17:41:00 example.com example: This is a test message"
            )
        )
        == "2025-07-20T17:41:00 NOTICE [example.com] example - This is a test message"
    )
