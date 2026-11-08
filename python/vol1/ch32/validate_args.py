"""Check a tool call's arguments against the tool's schema before running it."""

import json

TYPES = {"number": (int, float), "integer": (int,), "string": (str,), "boolean": (bool,)}


def validate_arguments(schema, arguments):
    """Return a list of problems (an empty list means the arguments are valid)."""
    params = schema["function"]["parameters"]
    allowed, problems = params["properties"], []
    for name in params.get("required", []):                       # 1. every required argument is present
        if name not in arguments:
            problems.append(f"missing required argument '{name}'")
    for name, value in arguments.items():
        if name not in allowed:                                    # 2. no unknown argument
            problems.append(f"unknown argument '{name}' (allowed: {sorted(allowed)})")
            continue
        rule = allowed[name]
        expected = TYPES.get(rule.get("type"))
        if expected and (not isinstance(value, expected) or isinstance(value, bool) and rule["type"] != "boolean"):  # 3. the right type
            problems.append(f"'{name}' must be a {rule['type']}, not {type(value).__name__} {value!r}")
            continue
        if "enum" in rule and value not in rule["enum"]:           # 4. one of the allowed values
            problems.append(f"'{name}' must be one of {rule['enum']}")
        if "minimum" in rule and value < rule["minimum"]:          # 5. inside the allowed range
            problems.append(f"'{name}' must be at least {rule['minimum']}")
        if "maximum" in rule and value > rule["maximum"]:
            problems.append(f"'{name}' must be at most {rule['maximum']}")
    return problems


def make_safe_call_tool(schemas, call_tool):
    """Wrap call_tool so that invalid arguments come back as an error the model can read."""
    by_name = {s["function"]["name"]: s for s in schemas}

    def safe_call_tool(name, arguments):
        if name in by_name:
            problems = validate_arguments(by_name[name], arguments)
            if problems:
                return json.dumps({"error": f"invalid call to {name}: " + "; ".join(problems)})
        return call_tool(name, arguments)
    return safe_call_tool
