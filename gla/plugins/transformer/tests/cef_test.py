from gla.plugins.transformer.cef_transformer import CefTransformer


def test_cef_transformer():
    cef = CefTransformer()

    test_cases = [
        {
            "input": "CEF:0|Vendor|Product|1.0|100|Test event|3|src=192.168.1.1 dst=10.0.0.2",
            "expected": "LOW [Vendor Product 1.0] Signature ID: 100 - Test event - "
            "Extensions: src=192.168.1.1 dst=10.0.0.2",
        },
        {
            "input": "CEF:1|Acme|Firewall|2.5|200|Blocked access|5|"
            "src=203.0.113.5 dst=198.51.100.1 msg=Blocked external access",
            "expected": "MEDIUM [Acme Firewall 2.5] Signature ID: 200 - Blocked access - "
            "Extensions: src=203.0.113.5 dst=198.51.100.1 msg=Blocked external access",
        },
        {
            "input": "CEF:2|SecurityCorp|IDS|3.0|300|Intrusion detected|8|"
            "src=10.10.1.1 dst=10.10.1.2 proto=TCP",
            "expected": "HIGH [SecurityCorp IDS 3.0] Signature ID: 300 - Intrusion detected - "
            "Extensions: src=10.10.1.1 dst=10.10.1.2 proto=TCP",
        },
        {
            "input": "CEF:0|Example|App|1.2|400|User login|9|src=192.168.2.2 user=jdoe",
            "expected": "VERY HIGH [Example App 1.2] Signature ID: 400 - User login - "
            "Extensions: src=192.168.2.2 user=jdoe",
        },
        {
            "input": "CEF:1|Network|Monitor|1.5|500|High CPU Usage|4|device=router1 cpu=95%",
            "expected": "MEDIUM [Network Monitor 1.5] Signature ID: 500 - High CPU Usage - "
            "Extensions: device=router1 cpu=95%",
        },
    ]

    for case in test_cases:
        input_log = case["input"]
        expected_result = case["expected"]
        result = cef.transform(input_log)

        if expected_result:
            assert (
                str(result) == expected_result
            ), f"Failed for input: {input_log}, Expected: {expected_result}, Got: {str(result)}"
        else:
            assert (
                result is None
            ), f"Failed for input: {input_log}, Expected: None, Got: {str(result)}"
