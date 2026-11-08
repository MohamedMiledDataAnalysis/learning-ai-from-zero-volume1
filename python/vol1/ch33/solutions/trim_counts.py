"""Exercise 33.3: messages and estimated tokens kept by trim_memory, for 1 to 7 turns.

    python python/vol1/ch33/solutions/trim_counts.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE.parents[1] / "ch29"), str(HERE.parents[2])]

from agent_core.brains import RuleBrain                    # noqa: E402
from agent_core.loop import run_agent                      # noqa: E402
from memory_tools import memory_size, trim_memory          # noqa: E402
from shop_rules import shop_rules                          # noqa: E402
from shop_tools import SCHEMAS, SYSTEM_PROMPT, call_tool   # noqa: E402

memory = run_agent("How much do 3 apples and 2 loaves of bread cost, in euros?", RuleBrain(shop_rules),
                   SCHEMAS, call_tool, SYSTEM_PROMPT, log=lambda m: None)["memory"]
print("turns kept | messages | estimated tokens")
for turns in range(1, 8):
    kept = trim_memory(memory, turns)
    print(f"{turns:>10} | {len(kept):>8} | {memory_size(kept):>16}")
