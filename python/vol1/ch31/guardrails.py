"""Guardrails for the Corner Shop agent: checks placed around the tools and around the brain."""

import difflib
import json
import re, sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1] / "ch29"))  # run alone
from shop_tools import PRICES, call_tool


# Guardrail 1 — a tool that helps the brain correct itself.
def call_tool_with_suggestions(name, arguments):
    """Like call_tool, but an unknown item comes back with the closest known name."""
    if name == "get_price":
        item = str(arguments.get("item", "")).strip().lower()
        if item not in PRICES:
            close = difflib.get_close_matches(item, list(PRICES), n=1, cutoff=0.6)
            hint = f" — did you mean '{close[0]}'?" if close else ""
            return json.dumps({"error": f"unknown item '{item}'{hint}"})
    return call_tool(name, arguments)


# Guardrails 2, 3 and 4 — a wrapper around any brain: it checks each reply before the loop sees it.
class GuardedBrain:
    def __init__(self, inner, max_repeats=3, allowed_numbers=()):
        self.inner = inner
        self.max_repeats = max_repeats
        self.allowed = {float(x) for x in allowed_numbers}   # numbers given in the question (the quantities)

    def next(self, memory, schemas):
        reply = self.inner.next(memory, schemas)
        if reply.get("tool_calls"):
            return self.check_arguments(memory, self.check_repeats(memory, reply))
        return self.check_answer(memory, reply)

    def check_repeats(self, memory, reply):
        """Guardrail 2: stop when the same call has already been made max_repeats times in a row."""
        new = json.dumps(reply["tool_calls"], sort_keys=True)
        previous = [json.dumps([c["function"] for c in m["tool_calls"]], sort_keys=True)
                    for m in memory if m["role"] == "assistant" and m.get("tool_calls")]
        repeats = 0
        for p in reversed(previous):
            if p != new:
                break
            repeats += 1
        if repeats >= self.max_repeats:
            return {"content": f"Stopped by guardrail: the same tool call was repeated {repeats} times.",
                    "tool_calls": []}
        return reply

    def known_numbers(self, memory):
        """Every number the agent is allowed to use: the question's quantities and every tool result."""
        known = set(self.allowed)
        for m in memory:
            if m["role"] == "tool":
                known |= {float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", m["content"])}
        return known

    def check_arguments(self, memory, reply):
        """Guardrail 3: every number passed to a tool must come from the question or a tool result."""
        if not reply.get("tool_calls"):
            return reply                                     # already stopped by guardrail 2
        known = self.known_numbers(memory)
        for c in reply["tool_calls"]:
            for name, value in c["arguments"].items():
                if isinstance(value, (int, float)) and float(value) not in known:
                    return {"content": f"Stopped by guardrail: {c['name']}({name}={value}) uses a number "
                                       f"that no tool returned.", "tool_calls": []}
        return reply

    def check_answer(self, memory, reply):
        """Guardrail 4: block an answer containing a number that no tool returned."""
        known = self.known_numbers(memory)
        numbers = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", reply["content"])]
        unknown = [x for x in numbers if x not in known]
        if unknown:
            return {"content": f"Answer blocked by guardrail: {unknown} not found in any tool result.",
                    "tool_calls": []}
        return reply


if __name__ == "__main__":
    print("This file holds functions only; run python/vol1/ch31/demo_failures.py to see them at work.")
