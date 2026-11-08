"""Chapter 26 — check that a model's JSON reply has the shape we asked for.

We ask the model for a trigger summary in this form (the schema):
    {"period": whole number 1-12,
     "test": "cumulative_default_ratio" or "arrears_90_ratio",
     "value": number between 0 and 1,
     "breached": true or false}
Then we test five replies of the kind models really produce.
"""

import json
import re

SCHEMA = {
    "period": {"type": int, "min": 1, "max": 12},
    "test": {"type": str, "allowed": ["cumulative_default_ratio", "arrears_90_ratio"]},
    "value": {"type": float, "min": 0.0, "max": 1.0},
    "breached": {"type": bool},
}


def extract_json(text):
    """Models often wrap JSON in ```json fences or add a sentence; keep only the {...} part."""
    match = re.search(r"\{.*\}", text, flags=re.S)
    if not match:
        raise ValueError("no JSON object found in the reply")
    return json.loads(match.group(0))


PLAIN = {int: "a whole number", float: "a number", str: "text", bool: "true or false"}


def check(data):
    """Return a list of problems; an empty list means the reply is valid."""
    problems = []
    for key, rule in SCHEMA.items():
        if key not in data:
            problems.append(f"missing key '{key}'")
            continue
        v = data[key]
        expected = rule["type"]
        # In Python, True is also an int: refuse booleans where a number is expected.
        ok_type = (isinstance(v, bool) if expected is bool else
                   isinstance(v, (int, float)) and not isinstance(v, bool) if expected is float else
                   isinstance(v, expected) and not isinstance(v, bool))
        if not ok_type:
            problems.append(f"'{key}' should be {PLAIN[expected]}, got {v!r}")
            continue
        if "min" in rule and not rule["min"] <= v <= rule["max"]:
            problems.append(f"'{key}'={v} is outside {rule['min']}-{rule['max']}")
        if "allowed" in rule and v not in rule["allowed"]:
            problems.append(f"'{key}'={v!r} is not one of {rule['allowed']}")
    for key in data:
        if key not in SCHEMA:
            problems.append(f"unexpected key '{key}'")
    return problems


def validate(text):
    try:
        data = extract_json(text)
    except (ValueError, json.JSONDecodeError) as e:
        return None, [f"not valid JSON: {e}"]
    return data, check(data)


REPLIES = {
    "A clean": '{"period": 10, "test": "arrears_90_ratio", "value": 0.01321, "breached": true}',
    "B fenced": 'Here is the summary:\n```json\n{"period": 10, "test": "arrears_90_ratio", '
                '"value": 0.01321, "breached": true}\n```',
    "C percent": '{"period": 10, "test": "arrears_90_ratio", "value": "1.32%", "breached": true}',
    "D missing": '{"period": 10, "test": "arrears_90_ratio", "value": 0.01321}',
    "E broken": "{'period': 10, 'test': 'arrears_90_ratio'}",
}

if __name__ == "__main__":
    for name, text in REPLIES.items():
        data, problems = validate(text)
        print(f"Reply {name:<10} -> {'VALID' if not problems else 'INVALID: ' + '; '.join(problems)}")
