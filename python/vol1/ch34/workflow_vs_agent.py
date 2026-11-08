"""The same question answered by a workflow (steps fixed in code) and by an agent (steps chosen by the brain).

    python python/vol1/ch34/workflow_vs_agent.py
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / "ch29"), str(HERE.parents[1])]

from agent_core.brains import RuleBrain                     # noqa: E402
from agent_core.loop import run_agent                       # noqa: E402
from shop_rules import shop_rules                           # noqa: E402
from shop_tools import SCHEMAS, SYSTEM_PROMPT, add, call_tool, gbp_to_eur, get_price, multiply  # noqa: E402


def shop_workflow(basket):
    """A workflow: the programmer wrote the order of the steps. It handles any basket, but only this task."""
    total = 0.0
    for item, quantity in basket.items():
        total = add(total, multiply(quantity, get_price(item)["price_gbp"])["result"])["result"]
    return gbp_to_eur(total)["amount_eur"]


print("WORKFLOW (steps fixed in code)")
print("  3 apples + 2 loaves of bread: €", shop_workflow({"apple": 3, "loaf of bread": 2}), sep="")
print("  1 milk + 2 cheese:            €", shop_workflow({"milk": 1, "cheese": 2}), sep="")

print("AGENT (steps chosen by the brain at each turn)")
out = run_agent("How much do 3 apples and 2 loaves of bread cost, in euros?", RuleBrain(shop_rules),
                SCHEMAS, call_tool, SYSTEM_PROMPT, log=lambda m: None)
print("  " + out["answer"])
print("  Steps chosen:", ", ".join(s["name"] for s in out["steps"] if s["type"] == "tool"))
