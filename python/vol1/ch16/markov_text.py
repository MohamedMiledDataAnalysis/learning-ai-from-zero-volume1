"""Chapter 16 — generate text one character at a time.

Model of order k: look at the last k characters, and choose the next character
in proportion to how often each character followed those k characters in the
training text (the prospectus).
"""

import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


def training_text():
    """The prospectus without its layout commands: plain words only."""
    # The January 2026 prospectus text, kept unchanged for Volume 1 (data/learning/corpus/).
    raw = Path("data/learning/corpus/prospectus_2026_01.md").read_text(encoding="utf-8")
    body = raw.split("---", 2)[2]                       # drop the settings block at the top
    body = re.sub(r"\\[a-z]+(\{[^}]*\})?", " ", body)   # drop commands such as \newpage
    body = re.sub(r"[|#*_`]", " ", body)                # drop table bars and Markdown marks
    body = re.sub(r"-{3,}:?", " ", body)
    return re.sub(r"\s+", " ", body).strip()


def fit(text, k):
    counts = defaultdict(Counter)
    for i in range(len(text) - k):
        counts[text[i:i + k]][text[i + k]] += 1
    return counts


def generate(counts, k, start, length, seed=7):
    rng = np.random.default_rng(seed)
    out = start
    while len(out) < length:
        options = counts.get(out[-k:]) if k else counts.get("")
        if not options:
            break
        chars = sorted(options)
        weights = np.array([options[c] for c in chars], dtype=float)
        out += chars[rng.choice(len(chars), p=weights / weights.sum())]
    return out


def main():
    text = training_text()
    print(f"Training text: {len(text):,} characters, {len(set(text))} different characters")
    counts1 = fit(text, 1)
    after_t = counts1["t"].most_common(3)
    print("After 't', the most frequent next characters:",
          ", ".join(f"'{c}' ({n})" for c, n in after_t))
    print()
    for k in (0, 1, 3, 6):
        counts = fit(text, k)
        start = text[:k] if k else ""
        sample = generate(counts, k, start, 110)
        print(f"Order {k}: {sample}")


if __name__ == "__main__":
    main()
