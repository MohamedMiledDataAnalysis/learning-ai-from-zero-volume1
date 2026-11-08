"""Run the Corner Shop agent with the fake brain.

    python python/vol1/ch29/shop_agent.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1])]          # this folder, and python/ for agent_core

from agent_core.brains import RuleBrain                     # noqa: E402
from agent_core.loop import run_agent                       # noqa: E402
from shop_rules import shop_rules                           # noqa: E402
from shop_tools import SCHEMAS, SYSTEM_PROMPT, call_tool    # noqa: E402

QUESTION = "How much do 3 apples and 2 loaves of bread cost, in euros?"

result = run_agent(QUESTION, RuleBrain(shop_rules), SCHEMAS, call_tool, SYSTEM_PROMPT, max_steps=10)
print("Answer:", result["answer"])
print("Stopped because:", result["stopped_because"])
print("Messages in memory:", len(result["memory"]))
