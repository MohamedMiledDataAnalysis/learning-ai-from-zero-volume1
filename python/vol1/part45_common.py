"""Shared helpers for Volume 1, Parts IV and V (chapters 21 to 27).

- prospectus_text(): the prospectus as plain text, page by page (the January 2026 text, kept unchanged
  in data/learning/corpus/ so that the figures of chapters 21 and 23 do not move when the deal's
  documents are revised)
- words(): split a text into lower-case words
- ask_model(): send messages to a language model in rules, replay, live or record mode
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "python"))

PENDING = "[Recording pending: run python record_all.py with Ollama installed, then rebuild]"
MODEL = "qwen2.5:7b"
OPTIONS = {"temperature": 0, "seed": 42, "num_ctx": 8192}


def prospectus_pages():
    """The text of each prospectus page (page 1 first), without the running header and page number."""
    from pypdf import PdfReader
    pages = []
    for page in PdfReader(REPO / "data" / "learning" / "corpus" / "prospectus_2026_01.pdf").pages:
        text = page.extract_text().replace("T est", "Test")      # repair a PDF kerning split
        lines = [ln for ln in text.splitlines()
                 if not ln.startswith("Thames Auto Receivables 2026-1 plc Prospectus")
                 and not re.fullmatch(r"Page \d+", ln.strip())]
        pages.append("\n".join(lines))
    return pages


def prospectus_text():
    return "\n".join(prospectus_pages())


def words(text):
    """Lower-case words and numbers; '90+' becomes '90', '£1,111' becomes '1' and '111'."""
    return re.findall(r"[a-z]+|[0-9]+", text.lower())


def parse_mode(default="replay"):
    """Read --mode from the command line: replay (default), live or record."""
    mode = default
    if "--mode" in sys.argv:
        mode = sys.argv[sys.argv.index("--mode") + 1]
    if mode not in ("replay", "live", "record"):
        raise SystemExit("--mode must be replay, live or record")
    return mode


def recording_exists(recording):
    return (REPO / "python" / "recordings" / f"{recording}.json").exists()


def ask_model(messages, recording, mode, fmt=None):
    """Send messages to the pinned model and return the reply text.

    replay  read the reply saved in python/recordings/<recording>.json (prints the pending line if absent)
    live    ask Ollama now, save nothing
    record  ask Ollama now and save the reply for replay
    Returns None when a replay file is missing (the caller then stops).
    """
    path = REPO / "python" / "recordings" / f"{recording}.json"
    if mode == "replay":
        if not path.exists():
            print(PENDING)
            return None
        return json.loads(path.read_text(encoding="utf-8"))["content"]
    import ollama
    kwargs = {"model": MODEL, "messages": messages, "options": OPTIONS}
    if fmt is not None:
        kwargs["format"] = fmt
    content = ollama.chat(**kwargs)["message"]["content"]
    if mode == "record":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"model": MODEL, "options": OPTIONS, "messages": messages,
                                    "content": content}, indent=2, ensure_ascii=False), encoding="utf-8")
    return content


def grade(answers, expected):
    """Compare the reader's answers with the expected ones and print a verdict for each.

    answers   list of strings typed on the command line
    expected  list of (question label, expected value, tolerance, section to reread)
    """
    if len(answers) != len(expected):
        labels = " ".join(f"<{q}>" for q, *_ in expected)
        raise SystemExit(f"Give {len(expected)} answer(s) on the command line: {labels}")
    score = 0
    for given, (label, value, tol, section) in zip(answers, expected):
        try:
            ok = abs(float(given.replace(",", "").rstrip("%")) - value) <= tol if tol is not None \
                else given.strip().lower() == str(value).lower()
        except ValueError:
            ok = False
        score += ok
        print(f"{label}: {'correct' if ok else f'not correct - reread section {section}'}")
    print(f"Practical task: {score}/{len(expected)}")
