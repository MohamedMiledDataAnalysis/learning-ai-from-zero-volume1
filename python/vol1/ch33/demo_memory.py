"""Short-term memory: size, trimming, summarising. Long-term memory: two runs, the second shorter.

    python python/vol1/ch33/demo_memory.py            both parts
    python python/vol1/ch33/demo_memory.py 1          part 1 only (short-term memory)
    python python/vol1/ch33/demo_memory.py 2          part 2 only (long-term memory)
"""

import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / "ch29"), str(HERE.parents[1])]

from agent_core.brains import RuleBrain                                  # noqa: E402
from agent_core.loop import run_agent                                    # noqa: E402
from memory_tools import LongTermMemory, memory_size, summarise_memory, trim_memory  # noqa: E402
from shop_rules import call, shop_rules                                  # noqa: E402
from shop_tools import SCHEMAS, SYSTEM_PROMPT, call_tool                 # noqa: E402

GOAL = "How much do 3 apples and 2 loaves of bread cost, in euros?"
quiet = lambda message: None                                              # noqa: E731
PARTS = sys.argv[1:] or ["1", "2"]

# Part 1 — short-term memory after the chapter 29 run.
if "1" in PARTS:
    memory = run_agent(GOAL, RuleBrain(shop_rules), SCHEMAS, call_tool, SYSTEM_PROMPT, log=quiet)["memory"]
    print("PART 1 — SHORT-TERM MEMORY")
    for i, m in enumerate(memory, start=1):
        what = m["content"] if m["role"] != "assistant" or not m["tool_calls"] else \
            "asks for " + m["tool_calls"][0]["function"]["name"]
        print(f"{i:>2}. {m['role']:<9} {what[:58]}")
    print(f"Messages: {len(memory)}, estimated tokens: {memory_size(memory)}")
    trimmed = trim_memory(memory, keep_last_turns=2)
    print(f"Trimmed to the last 2 turns: {len(trimmed)} messages, {memory_size(trimmed)} tokens")
    summary = summarise_memory(memory, keep_last_turns=2)
    print(f"Summarised: {len(summary)} messages, {memory_size(summary)} tokens")
    print("Summary note:", summary[2]["content"][:150] + "...")




# Part 2 — long-term memory: the brain skips get_price for any price it already knows.
def remembering_rules(memory):
    known = json.loads(memory[0]["content"].split("Facts saved from earlier runs: ")[1]) \
        if "Facts saved from earlier runs: " in memory[0]["content"] else {}
    looked_up = {json.loads(m["content"])["item"]: json.loads(m["content"])["price_gbp"]
                 for m in memory if m["role"] == "tool" and m["tool_name"] == "get_price"}
    prices = {**known, **looked_up}
    for item in ("apple", "loaf of bread"):
        if item not in prices:
            return call("get_price", item=item)
    results = [json.loads(m["content"]) for m in memory if m["role"] == "tool" and m["tool_name"] != "get_price"]
    n = len(results)
    if n == 0:
        return call("multiply", a=3, b=prices["apple"])
    if n == 1:
        return call("multiply", a=2, b=prices["loaf of bread"])
    if n == 2:
        return call("add", a=results[0]["result"], b=results[1]["result"])
    if n == 3:
        return call("gbp_to_eur", amount=results[2]["result"])
    return {"content": f"3 apples and 2 loaves of bread cost €{results[3]['amount_eur']:.2f}.", "tool_calls": []}


if "2" in PARTS:
    print()
    print("PART 2 — LONG-TERM MEMORY")
    with tempfile.TemporaryDirectory() as folder:
        store = LongTermMemory(Path(folder) / "shop_memory.json")
        for run in (1, 2):
            prompt = SYSTEM_PROMPT + " " + store.as_text()
            out = run_agent(GOAL, RuleBrain(remembering_rules), SCHEMAS, call_tool, prompt, log=quiet)
            tools = [s["name"] for s in out["steps"] if s["type"] == "tool"]
            print(f"Run {run}: {len(tools)} tool calls {tools}")
            print(f"       {out['answer']}")
            for s in out["steps"]:
                if s["type"] == "tool" and s["name"] == "get_price":
                    r = json.loads(s["result"])
                    store.remember(r["item"], r["price_gbp"])
        print("Saved facts:", json.dumps(store.facts, sort_keys=True))
