"""Practical task of chapter 31: Tool calls made by the looping brain with max_repeats=2.

    python python/vol1/ch31/check_ch31.py <your answer>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from part6_checker import grade  # noqa: E402,F401

from agent_core.brains import RuleBrain
from agent_core.loop import run_agent
from broken_brains import looping_brain
from guardrails import GuardedBrain
from shop_tools import SCHEMAS, SYSTEM_PROMPT, call_tool
out = run_agent('Q', GuardedBrain(RuleBrain(looping_brain), max_repeats=2), SCHEMAS, call_tool, SYSTEM_PROMPT, log=lambda m: None)
expected = sum(1 for s in out['steps'] if s['type'] == 'tool')

grade("Tool calls made by the looping brain with max_repeats=2", expected, "§ 31.4")
