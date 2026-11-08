"""Applied example: print the memory exactly as the brain receives it at step 4.

    python python/vol1/ch29/solutions/memory_after_step3.py
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE.parents[2])]

from agent_core.brains import RuleBrain                    # noqa: E402
from agent_core.loop import run_agent                      # noqa: E402
from shop_rules import shop_rules                          # noqa: E402
from shop_tools import SCHEMAS, SYSTEM_PROMPT, call_tool   # noqa: E402

out = run_agent("How much do 3 apples and 2 loaves of bread cost, in euros?", RuleBrain(shop_rules),
                SCHEMAS, call_tool, SYSTEM_PROMPT, max_steps=3, log=lambda m: None)
for m in out["memory"]:
    shown = {k: v for k, v in m.items() if k != "content" or m["role"] in ("user", "tool")}
    if m["role"] == "system":
        shown["content"] = m["content"][:40] + "..."
    print(json.dumps(shown, ensure_ascii=False))
