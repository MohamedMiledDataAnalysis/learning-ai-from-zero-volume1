"""Print the eight parts of the Corner Shop agent, before it runs.

    python python/vol1/ch28/show_parts.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / "ch29"), str(HERE.parents[1])]

from shop_tools import SCHEMAS, SYSTEM_PROMPT   # noqa: E402

GOAL = "How much do 3 apples and 2 loaves of bread cost, in euros?"
parts = [
    ("1. Goal and instructions", f"goal: {GOAL!r}; instructions: {len(SYSTEM_PROMPT)} characters"),
    ("2. Model (the brain)", "RuleBrain(shop_rules) in chapter 29; OllamaBrain('qwen2.5:7b') in chapter 30"),
    ("3. Tools", ", ".join(s["function"]["name"] for s in SCHEMAS)),
    ("4. Controller (the loop)", "run_agent() in python/agent_core/loop.py"),
    ("5. Memory", "a list of messages; it starts with 2: system + user"),
    ("6. Stopping rules", "final answer, or max_steps=10"),
    ("7. Guardrails", "none yet: chapter 31 adds four"),
    ("8. Log", "one line per step, printed by the loop"),
]
for name, value in parts:
    print(f"{name:<26} {value}")
