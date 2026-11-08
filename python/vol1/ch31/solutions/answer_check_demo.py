"""Exercise 31.5: a brain that answers at once with a guessed total. Which guardrail catches it?

    python python/vol1/ch31/solutions/answer_check_demo.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE.parents[1] / "ch29"), str(HERE.parents[2])]

from agent_core.brains import RuleBrain                    # noqa: E402
from agent_core.loop import run_agent                      # noqa: E402
from guardrails import GuardedBrain                        # noqa: E402
from shop_tools import SCHEMAS, SYSTEM_PROMPT, call_tool   # noqa: E402


def guessing_brain(memory):
    return {"content": "3 apples and 2 loaves of bread cost about €4.50.", "tool_calls": []}


GOAL = "How much do 3 apples and 2 loaves of bread cost, in euros?"
for title, brain in [("without guardrail", RuleBrain(guessing_brain)),
                     ("with GuardedBrain", GuardedBrain(RuleBrain(guessing_brain), allowed_numbers=(3, 2)))]:
    out = run_agent(GOAL, brain, SCHEMAS, call_tool, SYSTEM_PROMPT, log=lambda m: None)
    print(f"{title:<18} {out['answer']}")
