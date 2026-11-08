"""Exercise 29.5: new rules for '1 milk and 2 cheeses, in euros', run in the same loop.

    python python/vol1/ch29/solutions/milk_cheese_rules.py
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE.parents[2])]

from agent_core.brains import RuleBrain                    # noqa: E402
from agent_core.loop import run_agent                      # noqa: E402
from shop_rules import call                                # noqa: E402
from shop_tools import SCHEMAS, SYSTEM_PROMPT, call_tool   # noqa: E402


def milk_cheese_rules(memory):
    results = [json.loads(m["content"]) for m in memory if m["role"] == "tool"]
    n = len(results)
    if n == 0:
        return call("get_price", item="milk")
    if n == 1:
        return call("get_price", item="cheese")
    if n == 2:
        return call("multiply", a=2, b=results[1]["price_gbp"])      # 2 cheeses
    if n == 3:
        return call("add", a=results[0]["price_gbp"], b=results[2]["result"])   # 1 milk needs no multiply
    if n == 4:
        return call("gbp_to_eur", amount=results[3]["result"])
    return {"content": f"1 milk and 2 cheeses cost €{results[4]['amount_eur']:.2f}.", "tool_calls": []}


out = run_agent("How much do 1 milk and 2 cheeses cost, in euros?", RuleBrain(milk_cheese_rules),
                SCHEMAS, call_tool, SYSTEM_PROMPT)
print("Answer:", out["answer"])
