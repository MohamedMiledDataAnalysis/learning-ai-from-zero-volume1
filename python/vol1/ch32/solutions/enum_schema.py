"""Exercise 32.5: a tool with a limited choice of currencies, and three calls checked against it.

    python python/vol1/ch32/solutions/enum_schema.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_args import validate_arguments   # noqa: E402

CONVERT = {"type": "function", "function": {
    "name": "convert", "description": "Convert an amount in pounds to another currency at the shop's fixed rates.",
    "parameters": {"type": "object", "properties": {
        "amount": {"type": "number", "minimum": 0, "description": "Amount in pounds, 0 or more."},
        "currency": {"type": "string", "enum": ["EUR", "USD"], "description": "Target currency code."}},
        "required": ["amount", "currency"]}}}

for args in [{"amount": 3.75, "currency": "EUR"}, {"amount": 3.75, "currency": "JPY"}, {"amount": -1, "currency": "USD"}]:
    print(json.dumps(args), "->", validate_arguments(CONVERT, args) or "valid")
