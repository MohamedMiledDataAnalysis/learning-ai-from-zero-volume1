"""Practical task of chapter 33: Messages left after trim_memory(memory, keep_last_turns=3).

    python python/vol1/ch33/check_ch33.py <your answer>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from part6_checker import grade  # noqa: E402,F401

from agent_core.brains import RuleBrain
from agent_core.loop import run_agent
from memory_tools import trim_memory
from shop_rules import shop_rules
from shop_tools import SCHEMAS, SYSTEM_PROMPT, call_tool
memory = run_agent('Q', RuleBrain(shop_rules), SCHEMAS, call_tool, SYSTEM_PROMPT, log=lambda m: None)['memory']
expected = len(trim_memory(memory, 3))

grade("Messages left after trim_memory(memory, keep_last_turns=3)", expected, "§ 33.3")
