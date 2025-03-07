from plugins.transformer.json_transformer import JsonTransformer


def test_json_transformer():
    json = JsonTransformer()

    test_cases = [
        # ECS-compliant log (Elastic Common Schema)
        {
            "input": """{"@timestamp":"2019-08-06T14:08:40.199Z", "log.level":"DEBUG", "message":"init find form", "service.name":"spring-petclinic","process.thread.name":"http-nio-8080-exec-8","log.logger":"org.springframework.samples.petclinic.owner.OwnerController","transaction.id":"28b7fb8d5aba51f1","trace.id":"2869b25b5469590610fea49ac04af7da"}""",
            "expected": "2019-08-06T14:08:40.199000+00:00 DEBUG [spring-petclinic] org.springframework.samples.petclinic.owner.OwnerController - init find form",
        },
        # Log4j log format
        {
            "input": """{"timestamp":"2019-08-06T14:08:40.199Z", "level":"INFO", "message":"User login successful", "loggerName":"auth.service"}""",
            "expected": "2019-08-06T14:08:40.199000+00:00 INFO auth.service - User login successful",
        },
        # Syslog format
        {
            "input": """{"timestamp":"2019-08-06T14:08:40.199", "severity":"WARN", "msg":"Disk usage high", "host":"server-01"}""",
            "expected": "2019-08-06T14:08:40.199000 WARN [server-01] - Disk usage high",
        },
        # Missing fields (should still parse with defaults)
        {
            "input": """{"@timestamp":"2019-08-06T14:08:40.199Z", "message":"No log level", "service.name":"app"}""",
            "expected": "2019-08-06T14:08:40.199000+00:00 [app] - No log level",
        },
        # Invalid json
        {
            "input": """"2019-08-06T14:08:40.199Z", "message":"No log level", "service.name":"app"}""",
            "expected": None,
        },
    ]

    for case in test_cases:
        result = json._transform(case["input"])
        assert (
            str(result) == case["expected"]
            if case["expected"] is not None
            else result is None
        ), f"Test failed for input: {case['input']}"
