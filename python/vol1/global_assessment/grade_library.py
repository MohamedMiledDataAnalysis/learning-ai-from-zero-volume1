"""Grade Part F of the global assessment: your Library agent (Python), out of 15 points.

    python python/vol1/global_assessment/grade_library.py path/to/library_agent.py

Your file must define: find_book, days_late, fine, SCHEMAS, call_tool and run(question).
"""

import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "python"))


def load(path):
    spec = importlib.util.spec_from_file_location("reader_library_agent", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(points, label, test, reread):
    try:
        ok = bool(test())
    except NotImplementedError:                               # a TODO not filled in yet
        ok, label = False, f"{label} (not written yet)"
    except Exception as e:                                    # a crash scores 0, with the reason shown
        ok, label = False, f"{label} (crashed: {type(e).__name__}: {e})"
    print(f"{'PASS' if ok else 'FAIL'}  {points} pt  {label}" + ("" if ok else f"  -> reread {reread}"))
    return points if ok else 0


def grade(path):
    m = load(path)
    quiet = lambda message: None  # noqa: E731
    schema = {s["function"]["name"]: s["function"] for s in getattr(m, "SCHEMAS", [])}
    checks = [
        (1, "find_book finds 'The Silent River' (B001, due 2026-10-20)",
         lambda: m.find_book("The Silent River")["book_id"] == "B001"
         and m.find_book("the silent river")["due_date"] == "2026-10-20", "chapter 29"),
        (1, "find_book returns an error for an unknown title",
         lambda: "error" in m.find_book("The Missing Book"), "chapter 32"),
        (1, "days_late('B001', '2026-11-02') = 13", lambda: m.days_late("B001", "2026-11-02")["days_late"] == 13,
         "chapter 29"),
        (1, "days_late('B002', '2026-11-02') = 0 (not yet due)",
         lambda: m.days_late("B002", "2026-11-02")["days_late"] == 0, "chapter 32"),
        (1, "days_late('B005', '2026-11-02') = 0 (due that day)",
         lambda: m.days_late("B005", "2026-11-02")["days_late"] == 0, "chapter 32"),
        (1, "fine(13) = £2.60", lambda: abs(m.fine(13)["fine_gbp"] - 2.60) < 0.005, "chapter 29"),
        (1, "fine(0) = £0.00", lambda: abs(m.fine(0)["fine_gbp"]) < 0.005, "chapter 29"),
        (1, "fine(62) = £5.00 (the maximum)", lambda: abs(m.fine(62)["fine_gbp"] - 5.00) < 0.005, "chapter 32"),
        (1, "SCHEMAS describes find_book, days_late and fine",
         lambda: set(schema) == {"find_book", "days_late", "fine"}, "chapter 28"),
        (1, "each schema lists its required arguments",
         lambda: set(schema["find_book"]["parameters"]["required"]) == {"title"}
         and set(schema["days_late"]["parameters"]["required"]) == {"book_id", "on_date"}
         and set(schema["fine"]["parameters"]["required"]) == {"days"}, "chapter 32"),
        (1, "call_tool returns an error as text for an unknown tool",
         lambda: "error" in json.loads(m.call_tool("renew_book", {})), "chapter 32"),
        (2, "run: 'The Silent River' on 2026-11-02 -> £2.60",
         lambda: "£2.60" in m.run("What fine is owed for 'The Silent River' on 2026-11-02?", log=quiet),
         "chapters 29 and 30"),
        (2, "run: 'A Map of Small Islands' on 2026-11-02 -> £5.00",
         lambda: "£5.00" in m.run("What fine is owed for 'A Map of Small Islands' on 2026-11-02?", log=quiet),
         "chapters 29 and 31"),
    ]
    total = sum(check(*c) for c in checks)
    print(f"\nPart F score: {total} / 15")
    return total


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    grade(Path(sys.argv[1]).resolve())
