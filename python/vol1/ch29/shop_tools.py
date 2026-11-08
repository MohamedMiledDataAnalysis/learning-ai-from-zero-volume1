"""The Corner Shop tools: four plain functions, their descriptions for the model, and call_tool.

Every amount is money, so every result is rounded to the penny (2 decimal places).
"""

import csv
import json
from pathlib import Path

SHOP = Path(__file__).resolve().parents[3] / "data" / "learning" / "corner_shop"

with open(SHOP / "prices.csv", encoding="utf-8") as f:
    PRICES = {row["item"]: row for row in csv.DictReader(f)}
RATE = json.loads((SHOP / "exchange_rate.json").read_text(encoding="utf-8"))["rate"]


def get_price(item):
    """The price of one unit of an item, in pounds."""
    key = item.strip().lower()
    if key not in PRICES:
        return {"error": f"unknown item '{item}'"}
    return {"item": key, "price_gbp": float(PRICES[key]["price_gbp"]), "unit": PRICES[key]["unit"]}


def multiply(a, b):
    return {"result": round(a * b, 2)}


def add(a, b):
    return {"result": round(a + b, 2)}


def gbp_to_eur(amount):
    return {"amount_gbp": amount, "rate": RATE, "amount_eur": round(amount * RATE, 2)}


TOOLS = {"get_price": get_price, "multiply": multiply, "add": add, "gbp_to_eur": gbp_to_eur}

NUMBER = {"type": "number"}
SCHEMAS = [
    {"type": "function", "function": {
        "name": "get_price", "description": "Price in pounds of one unit of an item sold in the shop.",
        "parameters": {"type": "object", "properties": {"item": {"type": "string", "description": "Item name, e.g. 'apple'."}},
                       "required": ["item"]}}},
    {"type": "function", "function": {
        "name": "multiply", "description": "Multiply two numbers (result rounded to 2 decimals).",
        "parameters": {"type": "object", "properties": {"a": NUMBER, "b": NUMBER}, "required": ["a", "b"]}}},
    {"type": "function", "function": {
        "name": "add", "description": "Add two numbers (result rounded to 2 decimals).",
        "parameters": {"type": "object", "properties": {"a": NUMBER, "b": NUMBER}, "required": ["a", "b"]}}},
    {"type": "function", "function": {
        "name": "gbp_to_eur", "description": "Convert an amount in pounds to euros at the shop's fixed rate.",
        "parameters": {"type": "object", "properties": {"amount": NUMBER}, "required": ["amount"]}}},
]

SYSTEM_PROMPT = ("You are the Corner Shop assistant. Answer questions about the cost of shopping. "
                 "Always use the tools for prices and arithmetic; never guess a number. "
                 "Give the final answer in one sentence.")


def call_tool(name, arguments):
    """Run one tool and return its result as JSON text. Errors are returned as text too."""
    if name not in TOOLS:
        return json.dumps({"error": f"unknown tool '{name}'. Available tools: {sorted(TOOLS)}"})
    try:
        return json.dumps(TOOLS[name](**arguments))
    except TypeError as e:
        return json.dumps({"error": f"wrong arguments for {name}: {e}"})
