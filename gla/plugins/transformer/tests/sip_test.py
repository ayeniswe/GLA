from gla.analyzer.iterator import Unstructured
from gla.plugins.transformer.sip_transformer import SipTransformer


def test_sip_transformation(get_log_path, check_transformer_test_cases):
    # ARRANGE
    sip = SipTransformer()
    cases = [
        {
            "expected": "2010-06-07T17:12:23 [198.51.100.1:5060:udp] - Session: f81-d4-f6@example.com - "
                        "Sent a REGISTER-1 request from sip:alice@example.com;tag=76yhh "
                        "(198.51.100.1:5060:udp) to sip:example.com (198.51.100.10:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:24 [198.51.100.10:5060:udp] - Session: f81-d4-f6@example.com - "
                        "Received a REGISTER-1 200 response from sip:alice@example.com;tag=76yhh "
                        "(198.51.100.10:5060:udp) to sip:example.com;tag=reg-1xtr "
                        "(198.51.100.1:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:23 [198.51.100.1:5060:udp] - Session: tr-88h@example.com - "
                        "Received a INVITE-43 request from sip:alice@example.com;tag=a1-1 "
                        "(198.51.100.1:5060:udp) to sip:bob@example.net (203.0.113.200:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:23 [198.51.100.1:5060:udp] - Session: tr-88h@example.com - "
                        "Received a INVITE-43 request from sip:alice@example.com;tag=a1-1 "
                        "(198.51.100.1:5060:udp) to sip:bob@example.net (203.0.113.200:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:24 [203.0.113.200:5060:udp] - Session: tr-88h@example.com - "
                        "Sent a INVITE-43 100 response from sip:alice@example.com;tag=a1-1 "
                        "(203.0.113.200:5060:udp) to sip:bob@example.net (198.51.100.1:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:24 [203.0.113.200:5060:udp] - Session: tr-88h@example.com - "
                        "Sent a INVITE-43 request from sip:alice@example.com;tag=a1-1 "
                        "(203.0.113.200:5060:udp) to sip:bob@bob1.example.net (203.0.113.1:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:25 [203.0.113.200:5060:udp] - Session: tr-88h@example.com - "
                        "Sent a INVITE-43 request from sip:alice@example.com;tag=a1-1 "
                        "(203.0.113.200:5060:udp) to sip:bob@bob2.example.net ([2001:db8::9]:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:25 [203.0.113.1:5060:udp] - Session: tr-88h@example.com - "
                        "Received a INVITE-43 100 response from sip:alice@example.com;tag=a1-1 "
                        "(203.0.113.1:5060:udp) to sip:bob@example.net;tag=b1-1 "
                        "(203.0.113.200:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:26 [[2001:db8::9]:5060:udp] - Session: tr-88h@example.com - "
                        "Received a INVITE-43 100 response from sip:alice@example.com;tag=a1-1 "
                        "([2001:db8::9]:5060:udp) to sip:bob@example.net;tag=b2-2 "
                        "(203.0.113.200:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:26 [203.0.113.200:5060:udp] - Session: tr-88h@example.com - "
                        "Sent a INVITE-43 180 response from sip:alice@example.com;tag=a1-1 "
                        "(203.0.113.200:5060:udp) to sip:bob@example.net;b2-2 (198.51.100.1:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:27 [203.0.113.1:5060:udp] - Session: tr-88h@example.com - "
                        "Received a INVITE-43 180 response from sip:alice@example.com;tag=a1-1 "
                        "(203.0.113.1:5060:udp) to sip:bob@example.net;tag=b1-1 "
                        "(203.0.113.200:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:27 [203.0.113.200:5060:udp] - Session: tr-88h@example.com - "
                        "Sent a INVITE-43 180 response from sip:alice@example.com;tag=a1-1 "
                        "(203.0.113.200:5060:udp) to sip:bob@example.net;tag=b1-1 "
                        "(198.51.100.1:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:27 [203.0.113.1:5060:udp] - Session: tr-88h@example.com - "
                        "Received a INVITE-43 200 response from sip:alice@example.com;tag=a1-1 "
                        "(203.0.113.1:5060:udp) to sip:bob@example.net;tag=b1-1 "
                        "(203.0.113.200:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:28 [203.0.113.200:5060:udp] - Session: tr-88h@example.com - "
                        "Sent a INVITE-43 200 response from sip:alice@example.com;tag=a1-1 "
                        "(203.0.113.200:5060:udp) to sip:bob@example.net;tag=b1-1 "
                        "(198.51.100.1:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:28 [203.0.113.200:5060:udp] - Session: tr-88h@example.com - "
                        "Sent a CANCEL-43 request from sip:alice@example.com;tag=a1-1 "
                        "(203.0.113.200:5060:udp) to sip:bob@bob2.example.net "
                        "([2001:db8::9]:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:28 [[2001:db8::9]:5060:udp] - Session: tr-88h@example.com - "
                        "Received a INVITE-43 487 response from sip:alice@example.com;tag=a1-1 "
                        "([2001:db8::9]:5060:udp) to sip:bob@example.net;b2-2 "
                        "(203.0.113.200:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:29 [203.0.113.200:5060:udp] - Session: tr-88h@example.com - "
                        "Sent a ACK-43 request from sip:alice@example.com;tag=a1-1 "
                        "(203.0.113.200:5060:udp) to sip:bob@bob2.example.net "
                        "([2001:db8::9]:5060:udp)",
        },
        {
            "expected": "2010-06-07T17:12:30 [[2001:db8::9]:5060:udp] - Session: tr-88h@example.com - "
                        "Received a CANCEL-43 200 response from sip:alice@example.com;tag=a1-1 "
                        "([2001:db8::9]:5060:udp) to sip:bob@example.net;b2-2 "
                        "(203.0.113.200:5060:udp)",
        },
        {
            "expected": None,
        },
    ]
    path = get_log_path("test-sip.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    sip.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, sip)
