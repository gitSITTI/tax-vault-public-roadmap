import json
import importlib.util
import sys
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "taxvault" / "provenance_report.py"
spec = importlib.util.spec_from_file_location("shared_redaction_under_test", path)
core = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = core
spec.loader.exec_module(core)


def test_nested_json_quoted_keys_escaped_values_and_metrics():
    sensitive = ['short pass "quoted"', "tiny-key", "small-token"]
    value = {"Password": sensitive[0], "rows": [{"API_KEY": sensitive[1]}, {"access-token": sensitive[2]}], "metric": 0.45}
    result = core.redact(json.dumps(value))
    clean = json.loads(result)
    assert clean["metric"] == 0.45
    assert all(secret not in result for secret in sensitive)
    assert clean["rows"][0]["API_KEY"] == "[redacted]"


def test_text_query_encoded_key_header_and_url_userinfo():
    value = 'password="short pass" api-key=tinykey https://u:tinyurl@example.invalid/a?access%5Ftoken=tinyquery&metric=7 Authorization: Bearer tinybearer'
    result = core.redact(value)
    for secret in ["short pass", "tinykey", "tinyurl", "tinyquery", "tinybearer"]:
        assert secret not in result
    assert "metric=7" in result


def test_recursive_structure_redacts_secret_containers_without_mutating_input():
    source = {"secret": {"nested": "tiny"}, "metrics": [1, 2, True]}
    assert core.redact_object(source) == {"secret": "[redacted]", "metrics": [1, 2, True]}
    assert source["secret"] == {"nested": "tiny"}
