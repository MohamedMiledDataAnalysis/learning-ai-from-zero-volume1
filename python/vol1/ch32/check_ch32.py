"""Practical task of chapter 32: Number of problems found in multiply({"b": "x", "c": 1}).

    python python/vol1/ch32/check_ch32.py <your answer>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from part6_checker import grade  # noqa: E402,F401

from shop_tools import SCHEMAS
from validate_args import validate_arguments
expected = len(validate_arguments(SCHEMAS[1], {'b': 'x', 'c': 1}))

grade('Number of problems found in multiply({"b": "x", "c": 1})', expected, "§ 32.4")
