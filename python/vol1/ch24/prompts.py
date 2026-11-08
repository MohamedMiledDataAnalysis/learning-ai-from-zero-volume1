"""Chapter 24 — four ways to ask the same question about the deal.

Run:  python python/vol1/ch24/prompts.py show            print the four prompts
      python python/vol1/ch24/prompts.py ask --mode replay  print the model's recorded replies
      (--mode live asks Ollama now; --mode record asks it and saves the replies)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from part45_common import PENDING, REPO, ask_model, parse_mode, recording_exists  # noqa: E402

report = json.loads((REPO / "data/investor_reports/investor_report_2026_10.json").read_text(encoding="utf-8"))
FACTS = (f"Period {report['period']}. 90+ day arrears ratio: {report['triggers']['arrears_90_ratio']['value']:.4%}. "
         f"Limit: {report['triggers']['arrears_90_ratio']['limit']:.2%}. "
         f"Cumulative default ratio: {report['triggers']['cumulative_default_ratio']['value']:.4%}. "
         f"Limit: {report['triggers']['cumulative_default_ratio']['limit']:.2%}.")
QUESTION = "Has any trigger been breached this period?"

SYSTEM = ("You are a structured finance surveillance analyst. Answer only from the facts given. "
          "If the facts do not contain the answer, say so. Use British English.")

PROMPTS = {
    "1-bare": [
        {"role": "user", "content": QUESTION},
    ],
    "2-system-and-facts": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Facts: {FACTS}\n\nQuestion: {QUESTION}"},
    ],
    "3-few-shot": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": "Facts: Period 4. 90+ day arrears ratio: 0.1347%. Limit: 1.25%.\n\n"
                                    "Question: Has any trigger been breached this period?"},
        {"role": "assistant", "content": "No. The 90+ day arrears ratio is 0.13%, below the 1.25% limit."},
        {"role": "user", "content": f"Facts: {FACTS}\n\nQuestion: {QUESTION}"},
    ],
    "4-steps-and-json": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Facts: {FACTS}\n\nQuestion: {QUESTION}\n\n"
                                    "Work in two steps. Step 1: for each test, compare the value with its limit. "
                                    "Step 2: reply with JSON only, in this form: "
                                    '{"breached_tests": [names], "any_breach": true or false}'},
    ],
}

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "show"
    if action == "show":
        for name, messages in PROMPTS.items():
            print(f"=== Prompt {name} ===")
            for m in messages:
                print(f"[{m['role']}] {m['content']}")
            print()
    else:
        mode = parse_mode()
        if mode == "replay" and not all(recording_exists(f"vol1-ch24-{n}") for n in PROMPTS):
            print(PENDING)
            raise SystemExit(0)
        for name, messages in PROMPTS.items():
            print(f"=== Reply to prompt {name} ===")
            reply = ask_model(messages, f"vol1-ch24-{name}", mode)
            if reply is None:
                break
            print(reply.strip(), "\n")
