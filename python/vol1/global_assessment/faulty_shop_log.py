"""Global assessment, Part E — a Corner Shop run with three faults, printed as its log.

    python python/vol1/global_assessment/faulty_shop_log.py

The brain below is a deliberately faulty set of rules. The tools are the real
Corner Shop tools from chapter 29, and the loop is the book's loop, so the log
is exactly what the agent would print.
"""

import json
import sys
from pathlib import Path

VOL1 = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(VOL1 / "ch29"), str(VOL1.parent)]
from agent_core.brains import RuleBrain  # noqa: E402
from agent_core.loop import run_agent  # noqa: E402
from shop_tools import SCHEMAS, SYSTEM_PROMPT, call_tool  # noqa: E402

QUESTION = "How much do 2 litres of milk, 1 cheese and 1 butter cost, in euros?"


def call(name, **arguments):
    return {"content": "", "tool_calls": [{"name": name, "arguments": arguments}]}


def faulty_rules(memory):
    results = [json.loads(m["content"]) for m in memory if m["role"] == "tool"]
    n = len(results)
    if n == 0:
        return call("get_price", item="milk")
    if n == 1:
        return call("get_price", item="cheese")
    if n == 2:
        return call("get_price", item="butter")
    if n == 3:
        return call("multiply", a=2, b=results[0]["price_gbp"])
    if n == 4:
        return call("multiply", a=results[3]["result"], b=results[1]["price_gbp"])
    if n == 5:
        return call("add", a=results[4]["result"], b=1.50)
    return call("gbp_to_eur", amount=results[5]["result"])


if __name__ == "__main__":
    print(f"Question: {QUESTION}")
    if "--correct" in sys.argv:
        # The figures a correct agent would use: butter is not sold, so it reports that
        # and prices the two items the shop does sell.
        milk = json.loads(call_tool("multiply", {"a": 2, "b": 1.05}))["result"]
        total = json.loads(call_tool("add", {"a": milk, "b": 2.75}))["result"]
        euros = json.loads(call_tool("gbp_to_eur", {"amount": total}))["amount_eur"]
        print(f"Correct figures: 2 x 1.05 = {milk:.2f}; {milk:.2f} + 2.75 = {total:.2f} GBP; "
              f"{total:.2f} x 1.15 = {euros:.2f} EUR (butter is not sold)")
        sys.exit(0)
    result = run_agent(QUESTION, RuleBrain(faulty_rules), SCHEMAS, call_tool, SYSTEM_PROMPT,
                       max_steps=12, log=print)
    print(f"Answer: {result['answer']}")
    print(f"Stopped because: {result['stopped_because']}")
