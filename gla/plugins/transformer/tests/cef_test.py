from gla.analyzer.iterator import Unstructured
from gla.plugins.transformer.cef_transformer import CefTransformer


def test_cef_transformation(get_log_path, check_transformer_test_cases):
    # ARRANGE
    cef = CefTransformer()
    cases = [
        {
            "expected": "LOW [Vendor Product 1.0] Signature ID: 100 - Test event - "
            "Extensions: src=192.168.1.1 dst=10.0.0.2",
        },
        {
            "expected": "MEDIUM [Acme Firewall 2.5] Signature ID: 200 - Blocked access - "
            "Extensions: src=203.0.113.5 dst=198.51.100.1 msg=Blocked external access",
        },
        {
            "expected": "HIGH [SecurityCorp IDS 3.0] Signature ID: 300 - Intrusion detected - "
            "Extensions: src=10.10.1.1 dst=10.10.1.2 proto=TCP",
        },
        {
            "expected": "VERY HIGH [Example App 1.2] Signature ID: 400 - User login - "
            "Extensions: src=192.168.2.2 user=jdoe",
        },
        {
            "expected": "MEDIUM [Network Monitor 1.5] Signature ID: 500 - High CPU Usage - "
            "Extensions: device=router1 cpu=95%",
        },
        {"expected": None},
    ]
    path = get_log_path("test-cef.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    cef.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, cef)
