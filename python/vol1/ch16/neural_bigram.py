"""Chapter 16 — the same idea learned by a tiny neural network.

Instead of counting, the network learns a table of scores W (one row per
current character, one column per next character). Softmax turns a row of
scores into probabilities. Gradient descent adjusts W to make the real next
characters more probable: this is next-token prediction, the training task of
large language models, at the smallest possible scale.
"""

import numpy as np

from markov_text import training_text

text = training_text()
chars = sorted(set(text))
index = {c: i for i, c in enumerate(chars)}
V = len(chars)
x = np.array([index[c] for c in text[:-1]])      # current character
y = np.array([index[c] for c in text[1:]])       # the character that really comes next

W = np.zeros((V, V))                             # all scores start at 0: every character equally likely
print(f"Vocabulary: {V} characters | training pairs: {len(x):,}")
print(f"Loss if every character is equally likely: {np.log(V):.3f}")
for step in range(301):
    scores = W[x]                                            # one row of scores per training pair
    probs = np.exp(scores - scores.max(axis=1, keepdims=True))
    probs /= probs.sum(axis=1, keepdims=True)                # softmax
    loss = -np.log(probs[np.arange(len(y)), y]).mean()       # cross-entropy: surprise at the real next character
    if step in (0, 10, 50, 100, 300):
        print(f"  step {step:>3}: loss {loss:.3f}")
    grad = probs.copy()
    grad[np.arange(len(y)), y] -= 1                          # gradient of the loss for each pair
    G = np.zeros_like(W)
    np.add.at(G, x, grad / len(y))
    W -= 50.0 * G                                            # learning rate 50 (the table is tiny)

rng = np.random.default_rng(7)
c, out = "T", "T"
for _ in range(100):
    p = np.exp(W[index[c]] - W[index[c]].max())
    p /= p.sum()
    c = chars[rng.choice(V, p=p)]
    out += c
print("Sample:", out)
