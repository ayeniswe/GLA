from gla.analyzer.iterator import Unstructured
from gla.plugins.transformer.ncsa_transformer import NcsaTransformer


def test_ncsa_transformation_clf(get_log_path, check_transformer_test_cases):
   # ARRANGE
    ncsa = NcsaTransformer()
    cases = [
        {
            "expected": "2024-03-10T12:34:56+00:00 [192.168.1.1] - Request: GET /index.html HTTP/1.1 - "
                        "Status: 200 - Size: 1234",
        },
        {
            "expected": "2024-03-10T12:34:56+00:00 [[2001:db8::1]] - Request: POST /login HTTP/1.1 - "
                        "Status: 403 - Size: 567",
        },
        {
            "expected": "2024-03-10T12:34:56+00:00 [10.0.0.1] - Request: PUT /update HTTP/1.1 - "
                        "Status: 201 - Size: 890",
        },
    ]
    path = get_log_path("test-ncsa.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    ncsa.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, ncsa)

def test_ncsa_transformation_combined_clf(get_log_path, check_transformer_test_cases):
   # ARRANGE
    ncsa = NcsaTransformer()
    cases = [
        {
            "expected": "2024-03-10T12:34:56+00:00 [192.168.1.1] - Request: GET /index.html HTTP/1.1 - "
                        "Status: 200 - Size: 1234 - User-Agent: Mozilla/5.0",
        },
        {
            "expected": "2024-03-10T12:34:56+00:00 [203.0.113.5] - Request: POST /login HTTP/1.1 - "
                        "Status: 401 - Size: 456 - Referrer: https://example.com - "
                        "User-Agent: Mozilla/5.0 (Windows NT 10.0) - Cookie: session=abc123",
        },
        {
            "expected": "2024-03-10T12:34:56+00:00 [[2001:db8::2]] - Request: DELETE /account HTTP/1.1 - "
                        "Status: 204 - Size: 0 - User-Agent: curl/7.68.0",
        },
        {
            "expected": None,
        },
    ]
    path = get_log_path("test-ncsa2.log")
    iterator = Unstructured(path, "utf-8", "\n")
    # Select correct strategy
    ncsa.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, ncsa)