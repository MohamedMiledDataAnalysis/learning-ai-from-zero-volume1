"""Chapter 21 — learn small word vectors (embeddings) from the prospectus.

1. Count how often each pair of words appears close together (within 3 words).
2. Turn the counts into PPMI scores: how much more often than chance two words meet.
3. Compress each word's row of scores into 8 numbers with SVD: that is its vector.
4. Compare words with cosine similarity.
"""

import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from part45_common import prospectus_text, words  # noqa: E402

STOP = set("a an and are as at be by each for from in is it its of on or that the this to which with "
           "all any if not no than then their they has have been will".split())
WINDOW, DIMS, MIN_COUNT = 3, 8, 3


def cosine(u, v):
    return float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v)))


def build_vectors():
    tokens = [w for w in words(prospectus_text()) if w not in STOP and not w.isdigit()]
    freq = Counter(tokens)
    vocab = sorted(w for w, c in freq.items() if c >= MIN_COUNT)
    index = {w: i for i, w in enumerate(vocab)}
    co = np.zeros((len(vocab), len(vocab)))
    for i, w in enumerate(tokens):
        if w not in index:
            continue
        for j in range(max(0, i - WINDOW), min(len(tokens), i + WINDOW + 1)):
            if j != i and tokens[j] in index:
                co[index[w], index[tokens[j]]] += 1
    total = co.sum()
    row, col = co.sum(1, keepdims=True), co.sum(0, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log(co * total / (row * col))
    ppmi = np.where(np.isfinite(pmi) & (pmi > 0), pmi, 0.0)
    u, s, _ = np.linalg.svd(ppmi)
    vectors = u[:, :DIMS] * s[:DIMS]
    # SVD can return a column or its mirror image (all signs flipped); fix the sign so every computer agrees.
    signs = np.sign(vectors[np.abs(vectors).argmax(0), range(DIMS)])
    vectors = vectors * signs
    return vocab, index, vectors


def neighbours(word, vocab, index, vectors, n=4):
    v = vectors[index[word]]
    sims = [(cosine(v, vectors[i]), w) for i, w in enumerate(vocab) if w != word]
    return sorted(sims, key=lambda x: (-x[0], x[1]))[:n]


if __name__ == "__main__":
    vocab, index, vectors = build_vectors()
    print(f"Vocabulary: {len(vocab)} words seen at least {MIN_COUNT} times; each becomes {DIMS} numbers.")
    print("Vector for 'arrears':", np.round(vectors[index['arrears']], 2))
    for w in ["arrears", "principal", "reserve", "class"]:
        near = ", ".join(f"{x} ({s:.2f})" for s, x in neighbours(w, vocab, index, vectors))
        print(f"Closest to '{w}': {near}")
