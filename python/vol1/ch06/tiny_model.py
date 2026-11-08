"""Chapter 6 — learning by hand: predict a loan's interest rate from its credit score.

Model: rate = a + b * (score / 100). We try two guesses of (a, b), measure the error
of each with the mean squared error, then let the computer find the best a and b.
"""

import numpy as np
import pandas as pd

tape = pd.read_csv("data/loan_tape_cutoff.csv").drop_duplicates()
tape = tape[(tape.interest_rate_pct <= 30) & (tape.credit_score <= 999)]   # leave out the two impossible values

ids = ["TAR00011", "TAR00022", "TAR00051", "TAR00067", "TAR00080", "TAR00093"]
tiny = tape.set_index("loan_id").loc[ids, ["credit_score", "interest_rate_pct"]]
tiny["x"] = tiny.credit_score / 100
print("The six loans (x = credit score / 100, y = interest rate in %):")
for lid, r in tiny.iterrows():
    print(f"  {lid}  x = {r.x:.2f}   y = {r.interest_rate_pct:5.2f}")


def mse(a, b, data):
    """Mean squared error, computed exactly (used for the best lines)."""
    err = data.interest_rate_pct - (a + b * data.x)
    return float((err ** 2).mean())


def mse_by_hand(a, b, data):
    """The same calculation as you do it with a calculator: every number rounded to 2 decimals."""
    squares = []
    for lid, r in data.iterrows():
        p = round(a + b * r.x, 2)
        e = round(r.interest_rate_pct - p, 2)
        sq = round(e * e, 2)
        squares.append(sq)
        print(f"    {lid}: prediction {p:5.2f}  error {e:+6.2f}  squared {sq:6.2f}")
    print(f"    sum of squares = {sum(squares):.2f}, divided by {len(squares)} = {sum(squares) / len(squares):.2f}")


for a, b in [(20.0, -1.4), (18.0, -1.1)]:
    print(f"\nGuess a = {a}, b = {b}:")
    mse_by_hand(a, b, tiny)

b_best, a_best = np.polyfit(tiny.x, tiny.interest_rate_pct, 1)
print(f"\nBest line for the six loans: a = {a_best:.2f}, b = {b_best:.2f}, "
      f"mean squared error = {mse(a_best, b_best, tiny):.2f}")

tape["x"] = tape.credit_score / 100
b_all, a_all = np.polyfit(tape.x, tape.interest_rate_pct, 1)
print(f"Best line for all {len(tape):,} loans: a = {a_all:.2f}, b = {b_all:.2f}, "
      f"mean squared error = {mse(a_all, b_all, tape):.2f}")
print(f"Prediction for a score of 700 with the all-loans line: {a_all + b_all * 7:.2f}%")
