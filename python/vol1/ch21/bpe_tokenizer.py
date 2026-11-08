"""Chapter 21 — build a small byte-pair-encoding (BPE) tokeniser on the prospectus.

BPE starts with single characters and repeatedly glues together the pair of
symbols that appears most often. Each glued pair becomes a new token.
"""

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from part45_common import prospectus_text, words  # noqa: E402

N_MERGES = 200


def train_bpe(word_counts, n_merges):
    """Return the list of merges learnt, in order."""
    # Each word is a tuple of symbols, ending with '_' to mark the end of the word.
    vocab = {tuple(w) + ("_",): c for w, c in word_counts.items()}
    merges = []
    for _ in range(n_merges):
        pairs = Counter()
        for symbols, count in vocab.items():
            for a, b in zip(symbols, symbols[1:]):
                pairs[(a, b)] += count
        if not pairs:
            break
        # The most frequent pair; ties are broken alphabetically so the result never changes.
        best = min(pairs, key=lambda p: (-pairs[p], p))
        merges.append(best)
        new_vocab = {}
        for symbols, count in vocab.items():
            out, i = [], 0
            while i < len(symbols):
                if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == best:
                    out.append(symbols[i] + symbols[i + 1])
                    i += 2
                else:
                    out.append(symbols[i])
                    i += 1
            new_vocab[tuple(out)] = new_vocab.get(tuple(out), 0) + count
        vocab = new_vocab
    return merges


def tokenize_word(word, merges):
    """Apply the merges, in the order they were learnt, to one word."""
    symbols = list(word) + ["_"]
    for a, b in merges:
        i, out = 0, []
        while i < len(symbols):
            if i < len(symbols) - 1 and symbols[i] == a and symbols[i + 1] == b:
                out.append(a + b)
                i += 2
            else:
                out.append(symbols[i])
                i += 1
        symbols = out
    return symbols


def tokenize(text, merges):
    """Split a text into BPE tokens. Each distinct word is worked out once, then reused."""
    cache = {}
    out = []
    for w in words(text):
        if w not in cache:
            cache[w] = tokenize_word(w, merges)
        out.extend(cache[w])
    return out


if __name__ == "__main__":
    text = prospectus_text()
    counts = Counter(words(text))
    merges = train_bpe(counts, N_MERGES)

    print("First 10 merges learnt:")
    for i, (a, b) in enumerate(merges[:10], start=1):
        print(f"  {i:>2}. '{a}' + '{b}' -> '{a + b}'")

    sentence = "The 90+ day arrears ratio must not exceed 1.25%."
    print(f"\nSentence: {sentence}")
    print("Tokens:  ", " | ".join(tokenize(sentence, merges)))

    for w in ["arrears", "securitisation", "eligibility"]:
        print(f"'{w}' -> {tokenize_word(w, merges)}")

    n_chars = len("".join(words(text)))
    n_words = sum(counts.values())
    n_tokens = len(tokenize(text, merges))
    print(f"\nWhole prospectus: {n_chars:,} characters, {n_words:,} words, {n_tokens:,} BPE tokens "
          f"({N_MERGES} merges)")
    print(f"Tokens per word: {n_tokens / n_words:.2f}")
