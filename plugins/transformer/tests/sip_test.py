from plugins.transformer.sip_transformer import SipTransformer


def test_sip_transformation():
    sip = SipTransformer()

    test_cases = [
        {
            "input": "172 1275930743.699 R s REGISTER-1 sip:example.com 198.51.100.10:5060:udp "
            "198.51.100.1:5060:udp sip:example.com sip:alice@example.com;tag=76yhh "
            "f81-d4-f6@example.com - - c-tr-1",
            "expected": "2010-06-07T17:12:23 [198.51.100.1:5060:udp] - "
            "Session: f81-d4-f6@example.com - Sent a REGISTER-1 request from "
            "sip:alice@example.com;tag=76yhh (198.51.100.1:5060:udp) to sip:example.com "
            "(198.51.100.10:5060:udp)",
        },
        {
            "input": "173 1275930744.100 r r REGISTER-1 - 198.51.100.1:5060:udp "
            "198.51.100.10:5060:udp sip:example.com;tag=reg-1xtr sip:alice@example.com;tag=76yhh "
            "f81-d4-f6@example.com 200 - c-tr-1",
            "expected": "2010-06-07T17:12:24 [198.51.100.10:5060:udp] - "
            "Session: f81-d4-f6@example.com - Received a REGISTER-1 200 response from "
            "sip:alice@example.com;tag=76yhh (198.51.100.10:5060:udp) to "
            "sip:example.com;tag=reg-1xtr (198.51.100.1:5060:udp)",
        },
        {
            "input": "175 1275930743.699 R r INVITE-43 sip:bob@example.net 203.0.113.200:5060:udp "
            "198.51.100.1:5060:udp sip:bob@example.net sip:alice@example.com;tag=a1-1 "
            "tr-88h@example.com - s-1-tr -",
            "expected": "2010-06-07T17:12:23 [198.51.100.1:5060:udp] - Session: tr-88h@example.com"
            " - Received a INVITE-43 request from "
            "sip:alice@example.com;tag=a1-1 (198.51.100.1:5060:udp) "
            "to sip:bob@example.net (203.0.113.200:5060:udp)",
        },
        {
            "input": "175 1275930743.699 R r INVITE-43 sip:bob@example.net 203.0.113.200:5060:udp "
            "198.51.100.1:5060:udp sip:bob@example.net sip:alice@example.com;tag=a1-1 "
            'tr-88h@example.com - s-1-tr - Subject,13,"Call me ASAP!"',
            "expected": "2010-06-07T17:12:23 [198.51.100.1:5060:udp] - Session: tr-88h@example.com"
            " - Received a INVITE-43 request from sip:alice@example.com;tag=a1-1 "
            "(198.51.100.1:5060:udp) to sip:bob@example.net (203.0.113.200:5060:udp)",
        },
        {
            "input": "159 1275930744.001 r s INVITE-43 - 198.51.100.1:5060:udp "
            "203.0.113.200:5060:udp sip:bob@example.net sip:alice@example.com;tag=a1-1 "
            "tr-88h@example.com 100 s-1-tr -",
            "expected": "2010-06-07T17:12:24 [203.0.113.200:5060:udp] - "
            "Session: tr-88h@example.com - Sent a INVITE-43 100 response from "
            "sip:alice@example.com;tag=a1-1 (203.0.113.200:5060:udp) to "
            "sip:bob@example.net (198.51.100.1:5060:udp)",
        },
        {
            "input": "184 1275930744.998 R s INVITE-43 sip:bob@bob1.example.net "
            "203.0.113.1:5060:udp 203.0.113.200:5060:udp sip:bob@example.net "
            "sip:alice@example.com;tag=a1-1 tr-88h@example.com - s-1-tr c-1-tr",
            "expected": "2010-06-07T17:12:24 [203.0.113.200:5060:udp] - "
            "Session: tr-88h@example.com - Sent a INVITE-43 request from "
            "sip:alice@example.com;tag=a1-1 (203.0.113.200:5060:udp) to sip:bob@bob1.example.net "
            "(203.0.113.1:5060:udp)",
        },
        {
            "input": "186 1275930745.500 R s INVITE-43 sip:bob@bob2.example.net "
            "[2001:db8::9]:5060:udp 203.0.113.200:5060:udp sip:bob@example.net "
            "sip:alice@example.com;tag=a1-1 tr-88h@example.com - s-1-tr c-2-tr",
            "expected": "2010-06-07T17:12:25 [203.0.113.200:5060:udp] - "
            "Session: tr-88h@example.com - Sent a INVITE-43 request from "
            "sip:alice@example.com;tag=a1-1 (203.0.113.200:5060:udp) to sip:bob@bob2.example.net "
            "([2001:db8::9]:5060:udp)",
        },
        {
            "input": "172 1275930745.800 r r INVITE-43 - 203.0.113.200:5060:udp "
            "203.0.113.1:5060:udp sip:bob@example.net;tag=b1-1 sip:alice@example.com;tag=a1-1 "
            "tr-88h@example.com 100 s-1-tr c-1-tr",
            "expected": "2010-06-07T17:12:25 [203.0.113.1:5060:udp] - "
            "Session: tr-88h@example.com - Received a INVITE-43 100 response "
            "from sip:alice@example.com;tag=a1-1 (203.0.113.1:5060:udp) to "
            "sip:bob@example.net;tag=b1-1 (203.0.113.200:5060:udp)",
        },
        {
            "input": "174 1275930746.100 r r INVITE-43 - 203.0.113.200:5060:udp "
            "[2001:db8::9]:5060:udp sip:bob@example.net;tag=b2-2 sip:alice@example.com;tag=a1-1 "
            "tr-88h@example.com 100 s-1-tr c-2-tr",
            "expected": "2010-06-07T17:12:26 [[2001:db8::9]:5060:udp] - "
            "Session: tr-88h@example.com - Received a INVITE-43 100 response "
            "from sip:alice@example.com;tag=a1-1 ([2001:db8::9]:5060:udp) to "
            "sip:bob@example.net;tag=b2-2 (203.0.113.200:5060:udp)",
        },
        {
            "input": "170 1275930746.990 r s INVITE-43 - 198.51.100.1:5060:udp "
            "203.0.113.200:5060:udp sip:bob@example.net;b2-2 sip:alice@example.com;tag=a1-1 "
            "tr-88h@example.com 180 s-1-tr c-2-tr",
            "expected": "2010-06-07T17:12:26 [203.0.113.200:5060:udp] - "
            "Session: tr-88h@example.com - Sent a INVITE-43 180 response "
            "from sip:alice@example.com;tag=a1-1 (203.0.113.200:5060:udp) to "
            "sip:bob@example.net;b2-2 (198.51.100.1:5060:udp)",
        },
        {
            "input": "170 1275930747.100 r r INVITE-43 - 203.0.113.200:5060:udp "
            "203.0.113.1:5060:udp sip:bob@example.net;tag=b1-1 sip:alice@example.com;tag=a1-1 "
            "tr-88h@example.com 180 s-1-tr c-1-tr",
            "expected": "2010-06-07T17:12:27 [203.0.113.1:5060:udp] - "
            "Session: tr-88h@example.com - Received a INVITE-43 180 response "
            "from sip:alice@example.com;tag=a1-1 (203.0.113.1:5060:udp) "
            "to sip:bob@example.net;tag=b1-1 (203.0.113.200:5060:udp)",
        },
        {
            "input": "173 1275930747.300 r s INVITE-43 - 198.51.100.1:5060:udp "
            "203.0.113.200:5060:udp sip:bob@example.net;tag=b1-1 sip:alice@example.com;tag=a1-1 "
            "tr-88h@example.com 180 s-1-tr c-1-tr",
            "expected": "2010-06-07T17:12:27 [203.0.113.200:5060:udp] - "
            "Session: tr-88h@example.com - Sent a INVITE-43 180 response "
            "from sip:alice@example.com;tag=a1-1 (203.0.113.200:5060:udp) "
            "to sip:bob@example.net;tag=b1-1 (198.51.100.1:5060:udp)",
        },
        {
            "input": "172 1275930747.800 r r INVITE-43 - 203.0.113.200:5060:udp "
            "203.0.113.1:5060:udp sip:bob@example.net;tag=b1-1 sip:alice@example.com;tag=a1-1 "
            "tr-88h@example.com 200 s-1-tr c-1-tr",
            "expected": "2010-06-07T17:12:27 [203.0.113.1:5060:udp] - "
            "Session: tr-88h@example.com - Received a INVITE-43 200 response "
            "from sip:alice@example.com;tag=a1-1 (203.0.113.1:5060:udp) "
            "to sip:bob@example.net;tag=b1-1 (203.0.113.200:5060:udp)",
        },
        {
            "input": "173 1275930748.000 r s INVITE-43 - 198.51.100.1:5060:udp "
            "203.0.113.200:5060:udp sip:bob@example.net;tag=b1-1 sip:alice@example.com;tag=a1-1 "
            "tr-88h@example.com 200 s-1-tr c-1-tr",
            "expected": "2010-06-07T17:12:28 [203.0.113.200:5060:udp] - "
            "Session: tr-88h@example.com - Sent a INVITE-43 200 response "
            "from sip:alice@example.com;tag=a1-1 (203.0.113.200:5060:udp) "
            "to sip:bob@example.net;tag=b1-1 (198.51.100.1:5060:udp)",
        },
        {
            "input": "191 1275930748.201 R s CANCEL-43 sip:bob@bob2.example.net "
            "[2001:db8::9]:5060:udp 203.0.113.200:5060:udp sip:bob@example.net;b2-2 "
            "sip:alice@example.com;tag=a1-1 tr-88h@example.com - s-1-tr c-2-tr",
            "expected": "2010-06-07T17:12:28 [203.0.113.200:5060:udp] - "
            "Session: tr-88h@example.com - Sent a CANCEL-43 request "
            "from sip:alice@example.com;tag=a1-1 (203.0.113.200:5060:udp) "
            "to sip:bob@bob2.example.net ([2001:db8::9]:5060:udp)",
        },
        {
            "input": "170 1275930748.991 r r INVITE-43 - 203.0.113.200:5060:udp "
            "[2001:db8::9]:5060:udp sip:bob@example.net;b2-2 sip:alice@example.com;tag=a1-1 "
            "tr-88h@example.com 487 s-1-tr c-2-tr",
            "expected": "2010-06-07T17:12:28 [[2001:db8::9]:5060:udp] - "
            "Session: tr-88h@example.com - Received a INVITE-43 487 response "
            "from sip:alice@example.com;tag=a1-1 ([2001:db8::9]:5060:udp) "
            "to sip:bob@example.net;b2-2 (203.0.113.200:5060:udp)",
        },
        {
            "input": "188 1275930749.455 R s ACK-43 sip:bob@bob2.example.net "
            "[2001:db8::9]:5060:udp 203.0.113.200:5060:udp sip:bob@example.net;b2-2 "
            "sip:alice@example.com;tag=a1-1 tr-88h@example.com - s-1-tr c-2-tr",
            "expected": "2010-06-07T17:12:29 [203.0.113.200:5060:udp] - "
            "Session: tr-88h@example.com - Sent a ACK-43 request from "
            "sip:alice@example.com;tag=a1-1 (203.0.113.200:5060:udp) to sip:bob@bob2.example.net "
            "([2001:db8::9]:5060:udp)",
        },
        {
            "input": "170 1275930750.001 r r CANCEL-43 - 203.0.113.200:5060:udp "
            "[2001:db8::9]:5060:udp sip:bob@example.net;b2-2 sip:alice@example.com;tag=a1-1 "
            "tr-88h@example.com 200 s-1-tr c-2-tr",
            "expected": "2010-06-07T17:12:30 [[2001:db8::9]:5060:udp] - "
            "Session: tr-88h@example.com - Received a CANCEL-43 200 response "
            "from sip:alice@example.com;tag=a1-1 ([2001:db8::9]:5060:udp) "
            "to sip:bob@example.net;b2-2 (203.0.113.200:5060:udp)",
        },
    ]

    for case in test_cases:
        input_log = case["input"]
        expected_result = case["expected"]
        result = sip.transform(input_log)

        if expected_result:
            assert (
                str(result) == expected_result
            ), f"Failed for input: {input_log}, Expected: {expected_result}, Got: {str(result)}"
        else:
            assert (
                result is None
            ), f"Failed for input: {input_log}, Expected: None, Got: {str(result)}"
