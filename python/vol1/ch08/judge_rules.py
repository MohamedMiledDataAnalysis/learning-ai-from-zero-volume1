"""Chapter 8 — judging simple prediction rules on all the loans of the tape.

Question: which loans will fall 3 or more instalments behind (90+ days in arrears)
at some point in 2026? The answer is known: it is in data/loan_performance.csv.
We test three rules against it, then show what overfitting looks like.
"""

import numpy as np
import pandas as pd

tape = pd.read_csv("data/loan_tape_cutoff.csv").drop_duplicates().set_index("loan_id")
perf = pd.read_csv("data/loan_performance.csv")
# Label: 1 if the loan reached 3 or more instalments in arrears in 2026 (a defaulted loan counts: it passed 3 first).
label = (perf.groupby("loan_id").instalments_in_arrears.max() >= 3).astype(int)
tape["went_90plus"] = label

print(f"Loans: {len(tape):,}. Reached 90+ days in arrears in 2026: {tape.went_90plus.sum()} "
      f"({tape.went_90plus.mean():.2%})")


def judge(name, predicted, actual):
    tp = int(((predicted == 1) & (actual == 1)).sum())
    fp = int(((predicted == 1) & (actual == 0)).sum())
    fn = int(((predicted == 0) & (actual == 1)).sum())
    tn = int(((predicted == 0) & (actual == 0)).sum())
    accuracy = (tp + tn) / len(actual)
    precision = tp / (tp + fp) if tp + fp else float("nan")
    recall = tp / (tp + fn) if tp + fn else float("nan")
    print(f"\n{name}")
    print(f"  TP {tp:>4}  FP {fp:>4}  FN {fn:>4}  TN {tn:>5}")
    prec = "undefined (no loan predicted bad)" if tp + fp == 0 else f"{precision:.2%}"
    print(f"  accuracy {accuracy:.2%}   precision {prec}   recall {recall:.2%}")


y = tape.went_90plus
judge("Rule 0 — predict that no loan goes 90+", pd.Series(0, index=tape.index), y)
judge("Rule 1 — credit score below 700", (tape.credit_score < 700).astype(int), y)
judge("Rule 2 — borrower in the North West", (tape.region == "North West").astype(int), y)

# Overfitting: split the loans at random into a training set (70%) and a test set (30%).
rng = np.random.default_rng(8)
in_train = rng.random(len(tape)) < 0.70
train, test = tape[in_train], tape[~in_train]
print(f"\nTraining set: {len(train):,} loans ({train.went_90plus.sum()} went 90+). "
      f"Test set: {len(test):,} loans ({test.went_90plus.sum()} went 90+).")
memorised = set(train.index[train.went_90plus == 1])
judge("Rule M on the training set — 'bad if its loan_id is on my list of bad training loans'",
      pd.Series(train.index.isin(memorised).astype(int), index=train.index), train.went_90plus)
judge("Rule M on the test set",
      pd.Series(test.index.isin(memorised).astype(int), index=test.index), test.went_90plus)
judge("Rule 1 on the training set", (train.credit_score < 700).astype(int), train.went_90plus)
judge("Rule 1 on the test set", (test.credit_score < 700).astype(int), test.went_90plus)

# The applied example of Section 8.7: a stricter threshold on the full set of loans.
judge("Rule 3 — credit score below 650", (tape.credit_score < 650).astype(int), y)
