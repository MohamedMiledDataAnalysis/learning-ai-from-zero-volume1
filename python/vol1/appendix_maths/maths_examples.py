"""Appendix C — every worked example of the maths refresher, computed from the book's data.

    python python/vol1/appendix_maths/maths_examples.py [section]

Sections: percent, weighted, powers, sum, vectors, slope, probability, spread. No argument prints all.
"""

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[3]
DATA = REPO / "data"


def percent():
    rep = json.loads((DATA / "investor_reports" / "investor_report_2026_10.json").read_text(encoding="utf-8"))
    a90 = rep["arrears"]["3_instalments"]["balance"]
    pool = rep["pool"]["closing_balance"]
    terms = json.loads((DATA / "deal_terms.json").read_text(encoding="utf-8"))
    a = terms["initial_note_balances"]["A"]
    initial = terms["initial_pool_balance"]
    print(f"90+ arrears ratio, October 2026: {a90:,.2f} / {pool:,.2f} = {a90 / pool:.6f} = {a90 / pool:.2%}")
    print(f"Class A share of the notes: {a:,.2f} / {initial:,.2f} = {a / initial:.4f} = {a / initial:.2%}")
    old, new = 51494567.89, pool
    print(f"Pool balance change in October: ({new:,.2f} - {old:,.2f}) / {old:,.2f} = {(new - old) / old:.2%}")


def weighted():
    tape = pd.read_csv(REPO / "solutions" / "loan_tape_cutoff_clean.csv")
    five = tape.head(5)
    for r in five.itertuples():
        print(f"  {r.loan_id}: balance {r.current_balance:>10,.2f}  rate {r.interest_rate_pct:.2f}%")
    simple = five.interest_rate_pct.mean()
    wavg = (five.interest_rate_pct * five.current_balance).sum() / five.current_balance.sum()
    print(f"Simple average of the 5 rates: {simple:.4f}%")
    print(f"Weighted average (by balance): {wavg:.4f}%")
    whole = (tape.interest_rate_pct * tape.current_balance).sum() / tape.current_balance.sum()
    print(f"Weighted average of the whole pool: {whole:.2f}% (prospectus section 3)")


def powers():
    print(f"1.05 ** 3 = {1.05 ** 3:.6f}")
    print(f"10 ** -2 = {10 ** -2}")
    print(f"e = {math.e:.6f};  e ** 2 = {math.e ** 2:.6f}")
    print(f"ln(0.9) = {math.log(0.9):.6f}, so -ln(0.9) = {-math.log(0.9):.3f}")
    print(f"ln(0.1) = {math.log(0.1):.6f}, so -ln(0.1) = {-math.log(0.1):.3f}")
    for z in (-2, 0, 2):
        print(f"sigmoid({z}) = 1 / (1 + e^{-z}) = {1 / (1 + math.exp(-z)):.4f}")


def sums():
    tape = pd.read_csv(REPO / "solutions" / "loan_tape_cutoff_clean.csv")
    five = tape.current_balance.head(5).tolist()
    print("x1..x5 =", ", ".join(f"{x:,.2f}" for x in five))
    print(f"sum of x_i = {sum(five):,.2f}")
    print(f"sum over all 5,000 loans = {tape.current_balance.sum():,.2f}")


def vectors():
    q, k = np.array([1.0, 1.0]), np.array([0.0, 2.0])
    print(f"q = {q.tolist()}, k = {k.tolist()}, q . k = 1*0 + 1*2 = {q @ k:.1f}")
    print(f"length of k = sqrt(0^2 + 2^2) = {np.linalg.norm(k):.1f}")
    cos = q @ k / (np.linalg.norm(q) * np.linalg.norm(k))
    print(f"cosine(q, k) = {q @ k:.1f} / ({np.linalg.norm(q):.4f} x {np.linalg.norm(k):.1f}) = {cos:.4f}")
    W = np.array([[1.0, 0.0], [1.0, 2.0]])
    x = np.array([1.0, 1.0])
    print(f"W = {W.tolist()}, x = {x.tolist()}, W x = {(W @ x).tolist()}")
    A, B = np.array([[1, 2], [0, 1]]), np.array([[2, 0], [1, 3]])
    print(f"A = {A.tolist()}, B = {B.tolist()}, A B = {(A @ B).tolist()}")


def slope():
    def loss(w):
        return (w - 3) ** 2
    for w in (5.0, 3.0):
        h = 0.001
        numeric = (loss(w + h) - loss(w - h)) / (2 * h)
        print(f"L(w) = (w - 3)^2 at w = {w}: exact slope 2(w - 3) = {2 * (w - 3):.3f}, "
              f"measured slope = {numeric:.3f}")
    w = 5.0
    print(f"one gradient step with learning rate 0.1: w = {w} - 0.1 x {2 * (w - 3):.1f} = {w - 0.1 * 2 * (w - 3):.1f}")


def probability():
    loans = pd.read_csv(DATA / "learning" / "loans_2026.csv")
    n, bad = len(loans), int(loans.bad.sum())
    nw = loans[loans.north_west == 1]
    other = loans[loans.north_west == 0]
    print(f"P(bad) = {bad} / {n:,} = {bad / n:.4f}")
    print(f"P(good) = 1 - {bad / n:.4f} = {1 - bad / n:.4f}")
    print(f"P(bad | North West) = {int(nw.bad.sum())} / {len(nw)} = {nw.bad.mean():.4f}")
    print(f"P(bad | elsewhere)  = {int(other.bad.sum())} / {len(other):,} = {other.bad.mean():.4f}")


def spread():
    tape = pd.read_csv(REPO / "solutions" / "loan_tape_cutoff_clean.csv")
    five = tape.credit_score.head(5).astype(int).tolist()
    mean = sum(five) / 5
    dev2 = [(x - mean) ** 2 for x in five]
    var = sum(dev2) / 5
    print("scores:", five)
    print(f"mean = {sum(five)} / 5 = {mean:.1f}")
    print("squared deviations:", ", ".join(f"{d:.2f}" for d in dev2))
    print(f"variance (divide by n) = {sum(dev2):.2f} / 5 = {var:.2f}; standard deviation = {math.sqrt(var):.2f}")
    s = tape.credit_score
    print(f"all 5,000 loans: mean {s.mean():.1f}, standard deviation {s.std(ddof=0):.1f}")


SECTIONS = {"percent": percent, "weighted": weighted, "powers": powers, "sum": sums, "vectors": vectors,
            "slope": slope, "probability": probability, "spread": spread}

if __name__ == "__main__":
    for name in (sys.argv[1:] or SECTIONS):
        SECTIONS[name]()
