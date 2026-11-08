"""Global assessment, Part C — the five calculations, worked step by step.

    python python/vol1/global_assessment/part_c_answers.py

Every number in the printed solutions of Part C comes from this script.
"""

import math
import sys
from pathlib import Path

import pandas as pd

VOL1 = Path(__file__).resolve().parents[1]
REPO = VOL1.parents[1]
sys.path[:0] = [str(VOL1), str(VOL1 / "ch21")]
from bpe_tokenizer import N_MERGES, tokenize, train_bpe  # noqa: E402
from part45_common import prospectus_text, words  # noqa: E402
from collections import Counter  # noqa: E402


def sigmoid(z):
    return 1 / (1 + math.exp(-z))


def c1_c2():
    """C1: one neuron's output. C2: one gradient-descent step on the same neuron."""
    x1, x2 = 0.8, 1.0          # inputs (standardised loan-to-value, North West flag)
    w1, w2, b = -0.6, 1.5, -2.0
    y, rate = 1, 0.5           # the loan went bad; learning rate
    z = w1 * x1 + w2 * x2 + b
    p = sigmoid(z)
    print("C1  one neuron")
    print(f"    z = ({w1})({x1}) + ({w2})({x2}) + ({b}) = {z:.2f}")
    print(f"    p = 1 / (1 + e^{-z:.2f}) = {p:.4f}")
    g1, g2, gb = (p - y) * x1, (p - y) * x2, (p - y)
    print("C2  one gradient-descent step (cross-entropy loss, y = 1, learning rate 0.5)")
    print(f"    loss before = -ln({p:.4f}) = {-math.log(p):.4f}")
    print(f"    gradients: dw1 = (p - y) x1 = {g1:.4f}, dw2 = (p - y) x2 = {g2:.4f}, db = p - y = {gb:.4f}")
    nw1, nw2, nb = w1 - rate * g1, w2 - rate * g2, b - rate * gb
    print(f"    new w1 = {nw1:.4f}, new w2 = {nw2:.4f}, new b = {nb:.4f}")
    p2 = sigmoid(nw1 * x1 + nw2 * x2 + nb)
    print(f"    new p = {p2:.4f}, loss after = {-math.log(p2):.4f}")


def c3():
    """C3: precision and recall of the rule 'flag every North West loan' on the test set."""
    loans = pd.read_csv(REPO / "data" / "learning" / "loans_2026.csv")
    test = loans[loans.set == "test"]
    flag, bad = test.north_west == 1, test.bad == 1
    tp, fp = int((flag & bad).sum()), int((flag & ~bad).sum())
    fn, tn = int((~flag & bad).sum()), int((~flag & ~bad).sum())
    print("C3  rule 'flag every North West loan' on the 1,500 test loans")
    print(f"    TP = {tp}, FP = {fp}, FN = {fn}, TN = {tn}")
    print(f"    precision = {tp} / ({tp} + {fp}) = {tp / (tp + fp):.4f}")
    print(f"    recall    = {tp} / ({tp} + {fn}) = {tp / (tp + fn):.4f}")


def c4():
    """C4: attention of the word 'rising' over three words, with 2-number vectors."""
    q = (1.0, 1.0)                                            # query of 'rising'
    keys = {"pool": (1.0, 0.0), "arrears": (0.0, 2.0), "rising": (1.0, 1.0)}
    scale = math.sqrt(2)
    scores = {w: (q[0] * k[0] + q[1] * k[1]) / scale for w, k in keys.items()}
    total = sum(math.exp(s) for s in scores.values())
    print("C4  attention of 'rising' (query (1, 1)), scaled by sqrt(2) = 1.4142")
    for w, s in scores.items():
        print(f"    {w:<8} score = {s:.4f}   e^score = {math.exp(s):.4f}   weight = {math.exp(s) / total:.4f}")
    print(f"    sum of e^score = {total:.4f}")


def c5():
    """C5: token count of one sentence with the chapter 21 tokenizer, and its cost."""
    merges = train_bpe(Counter(words(prospectus_text())), N_MERGES)
    sentence = "The reserve fund must stay at its required amount."
    toks = tokenize(sentence, merges)
    requests, price = 50_000, 2.00                          # £2.00 per million input tokens
    cost = len(toks) * requests * price / 1_000_000
    print("C5  tokens and cost")
    print(f"    sentence: {sentence}")
    print(f"    tokens ({len(toks)}): {' | '.join(toks)}")
    print(f"    cost of sending it in {requests:,} requests at £{price:.2f} per million input tokens:")
    print(f"    {len(toks)} x {requests:,} = {len(toks) * requests:,} tokens -> £{cost:.2f}")


if __name__ == "__main__":
    c1_c2()
    c3()
    c4()
    c5()
