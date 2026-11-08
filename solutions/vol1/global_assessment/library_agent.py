"""Reference solution — global assessment, Part F: the Library agent (Python).

Grade it with:
    python python/vol1/global_assessment/grade_library.py solutions/vol1/global_assessment/library_agent.py

The eight parts of the skeleton (chapter 28) are marked in the comments.
"""

import csv
import json
import re
import sys
from datetime import date
from pathlib import Path


def repo_root(start=Path(__file__).resolve()):
    for folder in start.parents:
        if (folder / "python" / "agent_core").is_dir():
            return folder
    raise FileNotFoundError("run this file from inside the companion repository")


ROOT = repo_root()
sys.path.insert(0, str(ROOT / "python"))
from agent_core.brains import RuleBrain  # noqa: E402
from agent_core.loop import run_agent  # noqa: E402

LIBRARY = ROOT / "data" / "learning" / "library"
with open(LIBRARY / "books.csv", encoding="utf-8") as f:
    BOOKS = list(csv.DictReader(f))
RULES = json.loads((LIBRARY / "rules.json").read_text(encoding="utf-8"))


# Part 3 — tools: plain functions that return dictionaries.
def find_book(title):
    """The book whose title matches (ignoring case), or an error."""
    for book in BOOKS:
        if book["title"].lower() == title.strip().lower():
            return {"book_id": book["book_id"], "title": book["title"], "author": book["author"],
                    "due_date": book["due_date"]}
    return {"error": f"no book titled '{title}'"}


def days_late(book_id, on_date):
    """Whole days between the due date and on_date; 0 if the book is not late."""
    book = next((b for b in BOOKS if b["book_id"] == book_id), None)
    if book is None:
        return {"error": f"unknown book_id '{book_id}'"}
    late = (date.fromisoformat(on_date) - date.fromisoformat(book["due_date"])).days
    return {"book_id": book_id, "days_late": max(late, 0)}


def fine(days):
    """20p for each day late, never more than £5.00."""
    amount = min(days * RULES["fine_per_day_gbp"], RULES["maximum_fine_gbp"])
    return {"days": days, "fine_gbp": round(amount, 2)}


TOOLS = {"find_book": find_book, "days_late": days_late, "fine": fine}

SCHEMAS = [
    {"type": "function", "function": {
        "name": "find_book", "description": "Find a library book by its exact title.",
        "parameters": {"type": "object", "properties": {"title": {"type": "string"}}, "required": ["title"]}}},
    {"type": "function", "function": {
        "name": "days_late", "description": "Days a book is late on a date (YYYY-MM-DD); 0 if not late.",
        "parameters": {"type": "object", "properties": {"book_id": {"type": "string"}, "on_date": {"type": "string"}},
                       "required": ["book_id", "on_date"]}}},
    {"type": "function", "function": {
        "name": "fine", "description": "The fine in pounds for a number of days late.",
        "parameters": {"type": "object", "properties": {"days": {"type": "integer"}}, "required": ["days"]}}},
]

# Part 1 — goal and instructions.
SYSTEM_PROMPT = ("You are the library assistant. Use the tools for every date and amount; never guess. "
                 "Answer in one sentence.")


# Part 4 — controller: call_tool runs one tool and returns text, errors included (Part 7 — guardrail).
def call_tool(name, arguments):
    if name not in TOOLS:
        return json.dumps({"error": f"unknown tool '{name}'. Available tools: {sorted(TOOLS)}"})
    try:
        return json.dumps(TOOLS[name](**arguments))
    except (TypeError, ValueError) as e:
        return json.dumps({"error": f"wrong arguments for {name}: {e}"})


def call(name, **arguments):
    return {"content": "", "tool_calls": [{"name": name, "arguments": arguments}]}


# Part 2 — the brain (rules). It reads the question and the tool results in memory (Part 5).
def library_rules(memory):
    question = next(m["content"] for m in memory if m["role"] == "user")
    title = re.search(r"'([^']+)'", question).group(1)
    on_date = re.search(r"\d{4}-\d{2}-\d{2}", question).group(0)
    results = [json.loads(m["content"]) for m in memory if m["role"] == "tool"]
    if not results:
        return call("find_book", title=title)
    if "error" in results[-1]:                                  # Part 6 — stop on an error, do not guess
        return {"content": f"I cannot answer: {results[-1]['error']}.", "tool_calls": []}
    if len(results) == 1:
        return call("days_late", book_id=results[0]["book_id"], on_date=on_date)
    if len(results) == 2:
        return call("fine", days=results[1]["days_late"])
    return {"content": f"The fine for '{results[0]['title']}' on {on_date} is £{results[2]['fine_gbp']:.2f} "
                       f"({results[1]['days_late']} days late).", "tool_calls": []}


def run(question, log=print):
    """Part 6 — stopping rule: at most 6 steps. Part 8 — log: every step is printed."""
    return run_agent(question, RuleBrain(library_rules), SCHEMAS, call_tool, SYSTEM_PROMPT,
                     max_steps=6, log=log)["answer"]


if __name__ == "__main__":
    print(run("What fine is owed for 'The Silent River' on 2026-11-02?"))
