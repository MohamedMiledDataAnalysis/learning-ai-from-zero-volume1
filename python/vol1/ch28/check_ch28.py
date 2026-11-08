"""Practical task of chapter 28: How many messages are in memory after the Corner Shop run.

    python python/vol1/ch28/check_ch28.py <your answer>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from part6_checker import grade  # noqa: E402,F401

from agent_core.brains import RuleBrain
from agent_core.loop import run_agent
from shop_rules import shop_rules
from shop_tools import SCHEMAS, SYSTEM_PROMPT, call_tool
out = run_agent('How much do 3 apples and 2 loaves of bread cost, in euros?', RuleBrain(shop_rules), SCHEMAS, call_tool, SYSTEM_PROMPT, log=lambda m: None)
expected = len(out['memory'])

grade("How many messages are in memory after the Corner Shop run", expected, "§ 28.4")
