"""Chapter 16 — how much of a generated sample is copied from the training text?"""

from markov_text import fit, generate, training_text

text = training_text()
for k in (3, 6):
    sample = generate(fit(text, k), k, text[:k], 110)
    windows = [sample[i:i + 20] for i in range(len(sample) - 19)]   # every 20-character window of the sample
    copied = sum(w in text for w in windows)
    print(f"Order {k}: {copied} of {len(windows)} windows of 20 characters appear in the prospectus "
          f"({copied / len(windows):.0%})")
