"""Four brains that go wrong on purpose. Each imitates a mistake real models make."""

import json, sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1] / "ch29"))  # run alone
from shop_rules import call, shop_rules


def tool_results(memory):
    return [json.loads(m["content"]) for m in memory if m["role"] == "tool"]


def misspelling_brain(memory):
    """Failure 1: asks for 'aple'. If the error suggests a name, it retries with it; otherwise it gives up."""
    results = tool_results(memory)
    if not results:
        return call("get_price", item="aple")
    last = results[-1]
    if "error" in last and "did you mean" in last["error"]:
        return call("get_price", item=last["error"].split("'")[3])
    if "error" in last:
        return {"content": "I could not find the price of apples.", "tool_calls": []}
    return {"content": f"One apple costs £{last['price_gbp']:.2f}.", "tool_calls": []}


def missing_tool_brain(memory):
    """Failure 2: calls a tool that does not exist, then reads the error and uses the right one."""
    results = tool_results(memory)
    if not results:
        return call("convert_to_euros", amount=3.75)
    last = results[-1]
    if "error" in last:
        return call("gbp_to_eur", amount=3.75)
    return {"content": f"£3.75 is €{last['amount_eur']:.2f}.", "tool_calls": []}


def looping_brain(memory):
    """Failure 3: asks for the same price again and again and never answers."""
    return call("get_price", item="apple")


def inventing_brain(memory):
    """Failure 4: never looks up bread and invents a price of £0.95 a loaf for it."""
    results = tool_results(memory)
    n = len(results)
    if n == 0:
        return call("get_price", item="apple")
    if n == 1:
        return call("multiply", a=3, b=results[0]["price_gbp"])
    if n == 2:
        return call("add", a=results[1]["result"], b=1.90)          # 2 loaves at an invented £0.95
    if n == 3:
        return call("gbp_to_eur", amount=results[2]["result"])
    return {"content": f"3 apples and 2 loaves of bread cost €{results[3]['amount_eur']:.2f}.", "tool_calls": []}


__all__ = ["misspelling_brain", "missing_tool_brain", "looping_brain", "inventing_brain", "shop_rules"]


if __name__ == "__main__":
    print("This file holds functions only; run python/vol1/ch31/demo_failures.py to see them at work.")
