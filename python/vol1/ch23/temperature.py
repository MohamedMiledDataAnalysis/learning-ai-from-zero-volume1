"""Chapter 23 — how temperature changes the words a model picks.

A language model gives a probability for every possible next word. Here the
probabilities are fixed by hand for the text
    "The 90+ day arrears ratio must not ..."
We sample the next word 1,000 times at three temperatures and count the results.
"""

import numpy as np

next_words = ["exceed", "be", "rise", "fall", "sparkle"]
probs = np.array([0.62, 0.15, 0.10, 0.08, 0.05])
logits = np.log(probs)                       # the raw scores the model works with


def with_temperature(logits, t):
    """Divide the scores by t, then turn them back into probabilities (softmax)."""
    z = logits / t
    e = np.exp(z - z.max())
    return e / e.sum()


rng = np.random.default_rng(42)
print("Greedy choice (temperature 0): always", next_words[int(np.argmax(probs))])
for t in [0.2, 1.0, 2.0]:
    p = with_temperature(logits, t)
    draws = rng.choice(len(next_words), size=1000, p=p)
    counts = np.bincount(draws, minlength=len(next_words))
    row = "  ".join(f"{w} {pi:.3f} ({c})" for w, pi, c in zip(next_words, p, counts))
    print(f"t = {t}: {row}")
