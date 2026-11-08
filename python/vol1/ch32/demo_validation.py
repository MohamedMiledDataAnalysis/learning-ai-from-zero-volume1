"""Five tool calls through the validating wrapper.

    python python/vol1/ch32/demo_validation.py
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / "ch29")]

from shop_tools import SCHEMAS, call_tool                   # noqa: E402
from validate_args import make_safe_call_tool               # noqa: E402

safe = make_safe_call_tool(SCHEMAS, call_tool)
calls = [
    ("multiply", {"a": 3, "b": 0.45}),
    ("multiply", {"a": 3}),
    ("multiply", {"a": "three", "b": 0.45}),
    ("get_price", {"item": "apple", "shop": "Leeds"}),
    ("gbp_to_eur", {"amount": True}),
]
for name, args in calls:
    print(f"{name}({json.dumps(args)})")
    print("   ->", safe(name, args))
