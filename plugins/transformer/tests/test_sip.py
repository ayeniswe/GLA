from plugins.transformer.sip_transformer import SipTransformer


def test_sip_transformation():
    sip = SipTransformer()

    test_cases = [
        {
            "input": "172 1275930743.699 R s REGISTER-1 sip:example.com 198.51.100.10:5060:udp 198.51.100.1:5060:udp sip:example.com sip:alice@example.com;tag=76yhh f81-d4-f6@example.com - - c-tr-1",
            "expected": "2010-06-07T17:12:23 [198.51.100.1:5060:udp] - Session: f81-d4-f6@example.com - Sent a REGISTER-1 request from sip:alice@example.com;tag=76yhh (198.51.100.1:5060:udp) to sip:example.com (198.51.100.10:5060:udp)",
        },
        {
            "input": "173 1275930744.100 r r REGISTER-1 - 198.51.100.1:5060:udp 198.51.100.10:5060:udp sip:example.com;tag=reg-1xtr sip:alice@example.com;tag=76yhh f81-d4-f6@example.com 200 - c-tr-1",
            "expected": "2010-06-07T17:12:24 [198.51.100.10:5060:udp] - Session: f81-d4-f6@example.com - Received a REGISTER-1 200 response from sip:alice@example.com;tag=76yhh (198.51.100.10:5060:udp) to sip:example.com;tag=reg-1xtr (198.51.100.1:5060:udp)",
        },
        {
            "input": "175 1275930743.699 R r INVITE-43 sip:bob@example.net 203.0.113.200:5060:udp 198.51.100.1:5060:udp sip:bob@example.net sip:alice@example.com;tag=a1-1 tr-88h@example.com - s-1-tr -",
            "expected": "2010-06-07T17:12:23 [198.51.100.1:5060:udp] - Session: tr-88h@example.com - Received a INVITE-43 request from sip:alice@example.com;tag=a1-1 (198.51.100.1:5060:udp) to sip:bob@example.net (203.0.113.200:5060:udp)",
        },
        {
            "input": "175 1275930743.699 R r INVITE-43 sip:bob@example.net 203.0.113.200:5060:udp 198.51.100.1:5060:udp sip:bob@example.net sip:alice@example.com;tag=a1-1 tr-88h@example.com - s-1-tr - Subject,13,\"Call me ASAP!\"",
            "expected": "2010-06-07T17:12:23 [198.51.100.1:5060:udp] - Session: tr-88h@example.com - Received a INVITE-43 request from sip:alice@example.com;tag=a1-1 (198.51.100.1:5060:udp) to sip:bob@example.net (203.0.113.200:5060:udp)",
        },
    ]

    for case in test_cases:
        input_log = case["input"]
        expected_result = case["expected"]
        result = sip._transform(input_log)

        if expected_result:
            assert str(result) == expected_result, (
                f"Failed for input: {input_log}, Expected: {expected_result}, Got: {str(result)}"
            )
        else:
            assert result is None, (
                f"Failed for input: {input_log}, Expected: None, Got: {str(result)}"
            )
