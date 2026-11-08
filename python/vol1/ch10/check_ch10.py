"""Check your answer to the practical task of chapter 10.

Task: with the logistic regression of predict_default.py, use a threshold of 0.20.
What is the recall on the test set, in percent with 2 decimals?
Run:  python python/vol1/ch10/check_ch10.py --recall 12.34
"""

import argparse

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

parser = argparse.ArgumentParser()
parser.add_argument("--recall", type=float, required=True, help="recall in percent, e.g. 12.34")
answer = parser.parse_args().recall

loans = pd.read_csv("data/learning/loans_2026.csv")
loans["income_k"] = loans.annual_income / 1000
features = ["credit_score", "ltv_original_pct", "income_k", "used", "north_west"]
train, test = loans[loans.set == "train"], loans[loans.set == "test"]
model = LogisticRegression(C=np.inf, max_iter=100000, tol=1e-10).fit(train[features], train.bad)
flagged = model.predict_proba(test[features])[:, 1] >= 0.20
recall = 100 * (flagged & (test.bad == 1)).sum() / (test.bad == 1).sum()
if abs(answer - round(recall, 2)) < 0.005:
    print(f"Correct: recall at 0.20 is {recall:.2f}%.")
else:
    print("Not yet. Recall = TP / (TP + FN), counted on the test set only. Reread section 10.5.")
