"""Chapter 23 — does the deal pack fit in a model's context window?

We count tokens with the chapter 21 tokeniser. Real tokenisers produce fewer
tokens per word (they learn from far more text), so this count is an upper bound.
"""

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch21"))
from bpe_tokenizer import N_MERGES, tokenize, train_bpe  # noqa: E402
from part45_common import REPO, prospectus_text, words  # noqa: E402

merges = train_bpe(Counter(words(prospectus_text())), N_MERGES)

documents = {
    "Prospectus (9 pages)": prospectus_text(),
    "One investor report (Markdown)": (REPO / "data/investor_reports/investor_report_2026_10.md").read_text(encoding="utf-8"),
    "Loan tape (5,002 rows)": (REPO / "data/loan_tape_cutoff.csv").read_text(encoding="utf-8"),
}
WINDOW = 32_768          # tokens: qwen2.5:7b's trained window (this book sets num_ctx = 8,192)
total = 0
for name, text in documents.items():
    n = len(tokenize(text, merges))
    total += n
    print(f"{name:<32} {n:>9,} tokens  {'fits' if n <= WINDOW else 'does NOT fit'} in {WINDOW:,}")
print(f"{'All three together':<32} {total:>9,} tokens")
