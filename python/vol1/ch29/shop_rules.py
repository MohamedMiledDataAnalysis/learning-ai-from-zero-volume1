"""The fake brain: fixed rules that answer one question, with no AI at all."""

import json


def call(name, **arguments):
    return {"content": "", "tool_calls": [{"name": name, "arguments": arguments}]}


def shop_rules(memory):
    """Decide the next step from the tool results already in memory."""
    results = [json.loads(m["content"]) for m in memory if m["role"] == "tool"]
    n = len(results)                                       # how many tools have run so far
    if n == 0:
        return call("get_price", item="apple")
    if n == 1:
        return call("get_price", item="loaf of bread")
    if n == 2:
        return call("multiply", a=3, b=results[0]["price_gbp"])
    if n == 3:
        return call("multiply", a=2, b=results[1]["price_gbp"])
    if n == 4:
        return call("add", a=results[2]["result"], b=results[3]["result"])
    if n == 5:
        return call("gbp_to_eur", amount=results[4]["result"])
    euros = results[5]["amount_eur"]
    return {"content": f"3 apples and 2 loaves of bread cost €{euros:.2f}.", "tool_calls": []}
