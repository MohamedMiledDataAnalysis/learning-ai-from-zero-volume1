"""Chapter 27 — measure retrieval: does a passage that answers the question appear in the top 3?

Each test question comes with a phrase that only the answering passage contains,
read from the prospectus. 'Hit rate' = share of questions answered by one of the top 3 passages.
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from compare_search import bm25_scores, stem  # noqa: E402
from tar_agent.tools.prospectus import chunks, search_prospectus, tokens  # noqa: E402

TESTS = [
    ("What is the limit for the 90+ day arrears ratio?", "must not exceed 1.25%"),
    ("How much is the servicer paid?", "servicer fee of 1.00%"),
    ("What margin do the Class C notes pay?", "SONIA + 2.10%"),
    ("Which loans were eligible?", "Each loan met the following criteria"),
    ("When does principal switch to sequential payment?", "principal is paid sequentially"),
    ("What share of the pool is PCP?", "Share of PCP loans"),
    ("How is a defaulted loan defined?", "4 instalments in arrears"),
    ("Who is the trustee?", "Albion Trustee Services"),
]

docs = chunks()
stemmed_docs = [[stem(w) for w in d["tokens"]] for d in docs]
hits = {"exact": 0, "stemmed": 0}
print(f"{'Question':<52} exact  stemmed")
for question, phrase in TESTS:
    exact_texts = [r["text"] for r in search_prospectus(question)["results"]]
    scores = bm25_scores([stem(w) for w in tokens(question)], stemmed_docs)
    stem_texts = [docs[i]["text"] for i in np.argsort(-scores, kind="stable")[:3]]
    e, s = any(phrase in t for t in exact_texts), any(phrase in t for t in stem_texts)
    hits["exact"] += e
    hits["stemmed"] += s
    print(f"{question:<52} {'hit' if e else 'MISS':<5}  {'hit' if s else 'MISS'}")
n = len(TESTS)
print(f"\nHit rate (top 3): exact words {hits['exact']}/{n} = {hits['exact'] / n:.0%}, "
      f"stemmed {hits['stemmed']}/{n} = {hits['stemmed'] / n:.0%}")
