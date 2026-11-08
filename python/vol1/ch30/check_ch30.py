"""Practical task of chapter 30: Number of tool descriptions sent with each request.

    python python/vol1/ch30/check_ch30.py <your answer>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from part6_checker import grade  # noqa: E402,F401

from shop_tools import SCHEMAS
expected = len(SCHEMAS)

grade("Number of tool descriptions sent with each request", expected, "§ 30.2")
