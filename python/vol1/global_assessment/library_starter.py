"""Global assessment, Part F — your Library agent (Python). Copy this file and fill in every TODO.

    cp python/vol1/global_assessment/library_starter.py python/vol1/global_assessment/library_agent.py
    python python/vol1/global_assessment/grade_library.py python/vol1/global_assessment/library_agent.py

Data: data/learning/library/books.csv (book_id, title, author, due_date) and rules.json
(fine_per_day_gbp, maximum_fine_gbp). Dates are text in the form YYYY-MM-DD.

What each part must return (the grader checks these exact keys):
    find_book(title)            -> {"book_id", "title", "author", "due_date"}  or  {"error": "..."}
    days_late(book_id, on_date) -> {"book_id", "days_late"}  (0 when the book is not late)
    fine(days)                  -> {"days", "fine_gbp"}  (20p a day, never more than £5.00)
    SCHEMAS                     -> one schema per tool, with its required arguments
    call_tool(name, arguments)  -> JSON text; an unknown tool gives {"error": ...} as text
    run(question, log=print)    -> the final answer text, for questions such as
                                   "What fine is owed for 'The Silent River' on 2026-11-02?"
"""

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "python"))
from agent_core.brains import RuleBrain  # noqa: E402,F401
from agent_core.loop import run_agent  # noqa: E402,F401

LIBRARY = ROOT / "data" / "learning" / "library"
with open(LIBRARY / "books.csv", encoding="utf-8") as f:
    BOOKS = list(csv.DictReader(f))
RULES = json.loads((LIBRARY / "rules.json").read_text(encoding="utf-8"))


def find_book(title):
    raise NotImplementedError("TODO: find the book whose title matches, ignoring upper and lower case")


def days_late(book_id, on_date):
    raise NotImplementedError("TODO: days between due_date and on_date, never below 0")


def fine(days):
    raise NotImplementedError("TODO: fine_per_day_gbp x days, capped at maximum_fine_gbp, rounded to the penny")


SCHEMAS = []          # TODO: three schemas, as in chapter 29

SYSTEM_PROMPT = "TODO: one or two sentences of instructions"


def call_tool(name, arguments):
    raise NotImplementedError("TODO: run the tool and return JSON text; errors as text (chapter 32)")


def library_rules(memory):
    raise NotImplementedError("TODO: the fake brain: find_book, then days_late, then fine, then answer")


def run(question, log=print):
    raise NotImplementedError("TODO: run_agent with RuleBrain(library_rules) and a step limit")
