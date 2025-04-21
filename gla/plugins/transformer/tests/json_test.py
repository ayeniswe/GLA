from json import JSONDecodeError
from gla.analyzer.iterator import Mode, Structured
from gla.plugins.transformer.json_transformer import JsonTransformer
from pytest import raises

def test_json_transformation_ecs(get_log_path, check_transformer_test_cases):
   # ARRANGE
    json = JsonTransformer()
    cases = [
        {
            "expected": "2019-08-06T14:08:40.199000+00:00 DEBUG [spring-petclinic] "
                        "org.springframework.samples.petclinic.owner.OwnerController - init find form",
        },
    ]
    path = get_log_path("test-json-ecs.log")
    iterator = Structured(path, "utf-8", Mode.JSON)
    # Select correct strategy
    json.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, json)
    
def test_json_transformation_log4j(get_log_path, check_transformer_test_cases):
   # ARRANGE
    json = JsonTransformer()
    cases = [
        {
            "expected": "2019-08-06T14:08:40.199000+00:00 INFO auth.service "
                        "- User login successful",
        },
    ]
    path = get_log_path("test-json-log4j.log")
    iterator = Structured(path, "utf-8", Mode.JSON)
    # Select correct strategy
    json.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, json)
    
def test_json_transformation_syslog(get_log_path, check_transformer_test_cases):
   # ARRANGE
    json = JsonTransformer()
    cases = [
        {
            "expected": "2019-08-06T14:08:40.199000 WARN [server-01] - Disk usage high",
        },
    ]
    path = get_log_path("test-json-syslog.log")
    iterator = Structured(path, "utf-8", Mode.JSON)
    # Select correct strategy
    json.resolve((path, "utf-8"))

    # ACT-ASSERT
    check_transformer_test_cases(cases, iterator, json)


def test_json_transformation_invalid(get_log_path, check_transformer_test_cases):
    # ARRANGE
    json = JsonTransformer()
    path = get_log_path("test-json-invalid.log")

    # ACT-ASSERT
    with raises(JSONDecodeError):
        # ACT
        json.resolve((path, "utf-8"))