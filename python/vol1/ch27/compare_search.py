"""Chapter 27 — three ways to find the passage that answers "Which loans were eligible?".

1. BM25 on exact words (the agent's search_prospectus tool)
2. BM25 after stemming: cut word endings so 'eligible' and 'eligibility' both become 'elig'
3. Embeddings learnt from the prospectus only (TF-IDF + SVD, called LSA)
The passage we want is the one on page 7 that starts the list of eligibility criteria.
"""

import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tar_agent.tools.prospectus import chunks, search_prospectus, tokens  # noqa: E402

QUERY = "Which loans were eligible?"
WANTED = "Each loan met the following criteria"
SUFFIXES = ["ibility", "ible", "ities", "ity", "ations", "ation", "ing", "ies", "es", "s", "ed", "ly"]


def stem(word):
    """A very small stemmer: remove the first matching ending, keeping at least 3 letters."""
    for suffix in SUFFIXES:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def bm25_scores(query_words, docs_words, k1=1.5, b=0.75):
    n = len(docs_words)
    avg = sum(len(d) for d in docs_words) / n
    df = Counter(w for d in docs_words for w in set(d))
    scores = []
    for d in docs_words:
        tf, s = Counter(d), 0.0
        for w in query_words:
            if w in tf:
                idf = math.log(1 + (n - df[w] + 0.5) / (df[w] + 0.5))
                s += idf * tf[w] * (k1 + 1) / (tf[w] + k1 * (1 - b + b * len(d) / avg))
        scores.append(s)
    return np.array(scores)


def lsa_scores(query, docs, k=20):
    vocab = sorted({w for d in docs for w in d["tokens"]})
    ix = {w: i for i, w in enumerate(vocab)}
    m = np.zeros((len(docs), len(vocab)))
    for i, d in enumerate(docs):
        for w, c in Counter(d["tokens"]).items():
            m[i, ix[w]] = c
    idf = np.log(len(docs) / (m > 0).sum(0))
    u, s, vt = np.linalg.svd(m * idf, full_matrices=False)
    doc_vecs = u[:, :k] * s[:k]
    q = np.zeros(len(vocab))
    unknown = []
    for w in tokens(query):
        if w in ix:
            q[ix[w]] += idf[ix[w]]
        else:
            unknown.append(w)
    qv = q @ vt[:k].T
    sims = doc_vecs @ qv / (np.linalg.norm(doc_vecs, axis=1) * np.linalg.norm(qv) + 1e-12)
    return sims, unknown


def show(title, docs, scores):
    order = np.argsort(-scores, kind="stable")[:3]
    found = any(WANTED in docs[i]["text"] for i in order)
    print(f"{title}: {'FOUND' if found else 'missed'}")
    for rank, i in enumerate(order, start=1):
        print(f"  {rank}. page {docs[i]['page']}  score {scores[i]:.2f}  {docs[i]['text'][:58]}...")


if __name__ == "__main__":
    docs = chunks()
    print(f'Query: "{QUERY}"   query words: {tokens(QUERY)}\n')
    r = search_prospectus(QUERY)["results"]
    print(f"1. BM25, exact words: {'FOUND' if any(WANTED in x['text'] for x in r) else 'missed'}")
    for rank, x in enumerate(r, start=1):
        print(f"  {rank}. page {x['page']}  score {x['score']:.2f}  {x['text'][:58]}...")
    stems = [stem(w) for w in tokens(QUERY)]
    print(f"\n   stemmed query words: {stems}")
    show("2. BM25 with stemming", docs, bm25_scores(stems, [[stem(w) for w in d["tokens"]] for d in docs]))
    sims, unknown = lsa_scores(QUERY, docs)
    print(f"\n   words the LSA vectors have never seen: {unknown}")
    show("3. Embeddings learnt from the prospectus (LSA, 20 dimensions)", docs, sims)
