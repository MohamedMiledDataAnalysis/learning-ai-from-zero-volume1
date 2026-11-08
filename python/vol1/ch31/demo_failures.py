"""Run the four failures without guardrails, then with them.

    python python/vol1/ch31/demo_failures.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / "ch29"), str(HERE.parents[1])]

from agent_core.brains import RuleBrain                      # noqa: E402
from agent_core.loop import run_agent                        # noqa: E402
from broken_brains import (inventing_brain, looping_brain,   # noqa: E402
                           missing_tool_brain, misspelling_brain, shop_rules)
from guardrails import GuardedBrain, call_tool_with_suggestions  # noqa: E402
from shop_tools import SCHEMAS, SYSTEM_PROMPT, call_tool     # noqa: E402

GOAL = "How much do 3 apples and 2 loaves of bread cost, in euros?"
quiet = lambda message: None                                  # noqa: E731


def show(title, brain, tools=call_tool, max_steps=10):
    out = run_agent(GOAL, brain, SCHEMAS, tools, SYSTEM_PROMPT, max_steps=max_steps, log=quiet)
    tool_steps = sum(1 for s in out["steps"] if s["type"] == "tool")
    print(f"{title:<42} {tool_steps:>2} tool call{'s' if tool_steps != 1 else ' '} | {out['stopped_because']}\n    answer: {out['answer']}")


print("WITHOUT GUARDRAILS")
show("1. Misspelt item", RuleBrain(misspelling_brain))
show("2. Missing tool", RuleBrain(missing_tool_brain))
show("3. Never-ending loop (step limit 10)", RuleBrain(looping_brain))
show("4. Invented price", RuleBrain(inventing_brain))
print()
print("WITH GUARDRAILS")
show("0. Correct brain (guardrails stay silent)", GuardedBrain(RuleBrain(shop_rules), allowed_numbers=(3, 2)))
show("1. Misspelt item + suggestion", RuleBrain(misspelling_brain), tools=call_tool_with_suggestions)
show("3. Never-ending loop + repeat guard", GuardedBrain(RuleBrain(looping_brain)))
show("4. Invented price + argument check", GuardedBrain(RuleBrain(inventing_brain), allowed_numbers=(3, 2)))
