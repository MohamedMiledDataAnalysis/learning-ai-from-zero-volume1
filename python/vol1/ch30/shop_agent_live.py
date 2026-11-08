"""The Corner Shop agent with a real language model.

    python python/vol1/ch30/shop_agent_live.py --mode replay    play back the book's recording (default)
    python python/vol1/ch30/shop_agent_live.py --mode live      ask your local Ollama model
    python python/vol1/ch30/shop_agent_live.py --mode record    ask Ollama and save every reply
    python python/vol1/ch30/shop_agent_live.py --mode rules     the fake brain from chapter 29
"""

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / "ch29"), str(HERE.parents[1])]

from agent_core.brains import make_brain                     # noqa: E402
from agent_core.loop import run_agent                        # noqa: E402
from shop_rules import shop_rules                            # noqa: E402
from shop_tools import SCHEMAS, SYSTEM_PROMPT, call_tool     # noqa: E402

QUESTION = "How much do 3 apples and 2 loaves of bread cost, in euros?"
RECORDING = HERE.parents[1] / "recordings" / "vol1-ch30-shop.jsonl"

parser = argparse.ArgumentParser()
parser.add_argument("--mode", default="replay", choices=["rules", "replay", "live", "record"])
mode = parser.parse_args().mode

if mode == "replay" and not (RECORDING.exists() and RECORDING.stat().st_size):
    print("[Recording pending: run python record_all.py with Ollama installed, then rebuild]")
    sys.exit(0)

brain = make_brain(mode, RECORDING, rules=shop_rules)       # the only line that differs from chapter 29
result = run_agent(QUESTION, brain, SCHEMAS, call_tool, SYSTEM_PROMPT, max_steps=10)
print("Answer:", result["answer"])
print("Stopped because:", result["stopped_because"])
