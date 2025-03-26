from gla.plugins.transformer.ncsa_transformer import NcsaTransformer


def test_ncsa_transformation():
    ncsa = NcsaTransformer()

    test_cases = [
        {
            "input": "192.168.1.1 - - [10/Mar/2024:12:34:56 +0000] "
            '"GET /index.html HTTP/1.1" 200 1234',
            "expected": "2024-03-10T12:34:56+00:00 [192.168.1.1] - "
            "Request: GET /index.html HTTP/1.1 - Status: 200 - Size: 1234",
        },
        {
            "input": "[2001:db8::1] - - [10/Mar/2024:12:34:56 +0000] "
            '"POST /login HTTP/1.1" 403 567',
            "expected": "2024-03-10T12:34:56+00:00 [[2001:db8::1]] - "
            "Request: POST /login HTTP/1.1 - Status: 403 - Size: 567",
        },
        {
            "input": "10.0.0.1 user123 - [10/Mar/2024:12:34:56 +0000] "
            '"PUT /update HTTP/1.1" 201 890',
            "expected": "2024-03-10T12:34:56+00:00 [10.0.0.1] - "
            "Request: PUT /update HTTP/1.1 - Status: 201 - Size: 890",
        },
        # NCSA Combined Log Format test cases
        {
            "input": "192.168.1.1 - - [10/Mar/2024:12:34:56 +0000] "
            '"GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0" "-"',
            "expected": "2024-03-10T12:34:56+00:00 [192.168.1.1] - "
            "Request: GET /index.html HTTP/1.1 - Status: 200 - Size: 1234 - "
            "User-Agent: Mozilla/5.0",
        },
        {
            "input": "203.0.113.5 - admin [10/Mar/2024:12:34:56 +0000] "
            '"POST /login HTTP/1.1" 401 456 "https://example.com" '
            '"Mozilla/5.0 (Windows NT 10.0)" "session=abc123"',
            "expected": "2024-03-10T12:34:56+00:00 [203.0.113.5] - "
            "Request: POST /login HTTP/1.1 - Status: 401 - Size: 456 - "
            "Referrer: https://example.com - User-Agent: Mozilla/5.0 (Windows NT 10.0) - "
            "Cookie: session=abc123",
        },
        {
            "input": "[2001:db8::2] - - [10/Mar/2024:12:34:56 +0000] "
            '"DELETE /account HTTP/1.1" 204 0 "-" "curl/7.68.0" "-"',
            "expected": "2024-03-10T12:34:56+00:00 [[2001:db8::2]] - "
            "Request: DELETE /account HTTP/1.1 - Status: 204 - Size: 0 - User-Agent: curl/7.68.0",
        },
    ]

    for case in test_cases:
        input_log = case["input"]
        expected_result = case["expected"]
        result = ncsa.transform(input_log)

        if expected_result:
            assert (
                str(result) == expected_result
            ), f"Failed for input: {input_log}, Expected: {expected_result}, Got: {str(result)}"
        else:
            assert (
                result is None
            ), f"Failed for input: {input_log}, Expected: None, Got: {str(result)}"
