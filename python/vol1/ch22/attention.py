"""Chapter 22 — self-attention for a three-word sentence, step by step.

The numbers are small on purpose so you can check every line with a calculator
(the same numbers are worked by hand in section 22.4).
"""

import numpy as np

words = ["arrears", "keep", "rising"]

# Each word starts as a vector of 2 numbers (its embedding).
X = np.array([[1.0, 0.0],     # arrears
              [0.0, 1.0],     # keep
              [1.0, 1.0]])    # rising

# Three learnt matrices turn each embedding into a query, a key and a value.
W_q = np.array([[1.0, 0.0], [0.0, 1.0]])
W_k = np.array([[1.0, 1.0], [0.0, 1.0]])
W_v = np.array([[2.0, 0.0], [0.0, 1.0]])

Q, K, V = X @ W_q, X @ W_k, X @ W_v
print("Step 1 - queries, keys, values")
for w, q, k, v in zip(words, Q, K, V):
    print(f"  {w:<8} q={q}  k={k}  v={v}")

scores = Q @ K.T                       # each query compared with every key (dot product)
print("\nStep 2 - scores = q . k (row = word that looks, column = word looked at)")
print(np.round(scores, 3))

d = Q.shape[1]
scaled = scores / np.sqrt(d)           # divide by the square root of the vector length
print(f"\nStep 3 - scaled scores (divided by sqrt({d}) = {np.sqrt(d):.4f})")
print(np.round(scaled, 3))

weights = np.exp(scaled) / np.exp(scaled).sum(axis=1, keepdims=True)   # softmax, row by row
print("\nStep 4 - attention weights (softmax: each row adds up to 1)")
print(np.round(weights, 3))

output = weights @ V                   # each word's new vector: a weighted mix of the values
print("\nStep 5 - output = weights x values")
for w, o in zip(words, output):
    print(f"  {w:<8} {np.round(o, 3)}")
