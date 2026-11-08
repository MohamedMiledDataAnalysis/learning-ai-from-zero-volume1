"""The whole Corner Shop agent in one file, with its eight pieces labelled.

    python python/vol1/ch28/agent_8_pieces.py                  the rule brain (no AI, always the same)
    python python/vol1/ch28/agent_8_pieces.py --mode live      a real model (needs Ollama and qwen2.5:7b)
    python python/vol1/ch28/agent_8_pieces.py --mode inventing a brain that invents a price (piece 7 at work)
"""

import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[3] / "data" / "learning" / "corner_shop"

# ── PIECE 1 — GOAL AND INSTRUCTIONS ── (the flight plan)
GOAL = "How much do 3 apples and 2 loaves of bread cost, in euros?"
INSTRUCTIONS = ("You are the Corner Shop assistant. Always use the tools for prices and arithmetic; "
                "never guess a number. Give the final answer in one sentence.")

# ── PIECE 3 — TOOLS and their descriptions ── (the labelled controls)
PRICES = {}
for line in (DATA / "prices.csv").read_text(encoding="utf-8").splitlines()[1:]:
    item, price, unit = line.split(",")
    PRICES[item] = float(price)
RATE = json.loads((DATA / "exchange_rate.json").read_text(encoding="utf-8"))["rate"]

TOOLS = {
    "get_price": lambda item: {"item": item, "price_gbp": PRICES[item]},
    "multiply": lambda a, b: {"result": round(a * b, 2)},
    "add": lambda a, b: {"result": round(a + b, 2)},
    "gbp_to_eur": lambda amount: {"amount_eur": round(amount * RATE, 2)},
}
DESCRIPTIONS = [  # what the model reads to know each tool exists (shortened from chapter 29)
    {"type": "function", "function": {"name": "get_price", "description": "Price in pounds of one item.",
     "parameters": {"type": "object", "properties": {"item": {"type": "string"}}, "required": ["item"]}}},
    {"type": "function", "function": {"name": "multiply", "description": "Multiply two numbers.",
     "parameters": {"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}}}},
    {"type": "function", "function": {"name": "add", "description": "Add two numbers.",
     "parameters": {"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}}}},
    {"type": "function", "function": {"name": "gbp_to_eur", "description": "Convert pounds to euros.",
     "parameters": {"type": "object", "properties": {"amount": {"type": "number"}}}}},
]


# ── PIECE 2 — AI MODEL ── (the pilot)
def ask(name, **arguments):
    """The brain's way of writing a request for a tool."""
    return {"content": "", "tool_calls": [{"name": name, "arguments": arguments}]}


def rule_brain(memory):
    """A stand-in for the model: fixed rules, so the run is always the same. Chapter 29 explains it."""
    results = [json.loads(m["content"]) for m in memory if m["role"] == "tool"]
    n = len(results)                                    # how many tools have run so far
    if n == 0:
        return ask("get_price", item="apple")
    if n == 1:
        return ask("get_price", item="loaf of bread")
    if n == 2:
        return ask("multiply", a=3, b=results[0]["price_gbp"])
    if n == 3:
        return ask("multiply", a=2, b=results[1]["price_gbp"])
    if n == 4:
        return ask("add", a=results[2]["result"], b=results[3]["result"])
    if n == 5:
        return ask("gbp_to_eur", amount=results[4]["result"])
    return {"content": f"3 apples and 2 loaves of bread cost €{results[5]['amount_eur']:.2f}.",
            "tool_calls": []}


def inventing_brain(memory):
    """A faulty brain that skips the price list and invents £0.50 for an apple."""
    if not any(m["role"] == "tool" for m in memory):
        return ask("multiply", a=3, b=0.50)
    return {"content": "I could not finish.", "tool_calls": []}


def ollama_brain(memory):
    """A real language model on your computer. Swapping the brain is the only change."""
    import ollama
    reply = ollama.chat(model="qwen2.5:7b", messages=memory, tools=DESCRIPTIONS,
                        options={"temperature": 0, "seed": 42, "num_ctx": 8192})["message"]
    calls = [{"name": c["function"]["name"], "arguments": dict(c["function"]["arguments"])}
             for c in reply.get("tool_calls") or []]
    return {"content": reply.get("content") or "", "tool_calls": calls}


# ── PIECE 7 — GUARDRAIL ── (the checklists)
def guardrail(name, arguments, memory):
    """Refuse any number that the goal or an earlier tool result did not contain."""
    seen = {3.0, 2.0}  # the quantities in the goal
    for m in memory:
        if m["role"] == "tool":
            seen.update(float(v) for v in json.loads(m["content"]).values() if isinstance(v, (int, float)))
    invented = [v for v in arguments.values() if isinstance(v, (int, float)) and float(v) not in seen]
    return f"blocked: {invented} did not come from the goal or a tool" if invented else None


# ── PIECE 4 — CONTROLLER LOOP ── (fly-by-wire)
def run(brain, max_steps):
    # ── PIECE 5 — MEMORY ── (the flight log)
    memory = [{"role": "system", "content": INSTRUCTIONS}, {"role": "user", "content": GOAL}]
    for step in range(1, max_steps + 1):
        reply = brain(memory)                                       # the pilot decides
        memory.append({"role": "assistant", "content": reply["content"],
                       "tool_calls": [{"function": c} for c in reply["tool_calls"]]})
        # ── PIECE 6 — STOPPING RULES ── (landing)
        if not reply["tool_calls"]:
            log(step, f"[6 STOP] final answer: {reply['content']}")
            return reply["content"]
        for call in reply["tool_calls"]:
            name, arguments = call["name"], call["arguments"]
            refusal = guardrail(name, arguments, memory)
            result = {"error": refusal} if refusal else TOOLS[name](**arguments)
            memory.append({"role": "tool", "content": json.dumps(result)})
            shown = ", ".join(json.dumps(v) for v in arguments.values())
            log(step, f"[2 MODEL] asks {name}({shown})  "
                      f"{'[7 GUARD] ' + refusal if refusal else '[3 TOOL] -> ' + json.dumps(result)}  "
                      f"[5 MEMORY] {len(memory)} messages")
    log(max_steps, f"[6 STOP] step limit of {max_steps} reached: no answer")
    return None


# ── PIECE 8 — LOG ── (the black box)
def log(step, text):
    print(f"[8 LOG] step {step}  {text}")


if __name__ == "__main__":
    mode = sys.argv[sys.argv.index("--mode") + 1] if "--mode" in sys.argv else "rules"
    brain = {"rules": rule_brain, "live": ollama_brain, "inventing": inventing_brain}[mode]
    run(brain, max_steps=10)
