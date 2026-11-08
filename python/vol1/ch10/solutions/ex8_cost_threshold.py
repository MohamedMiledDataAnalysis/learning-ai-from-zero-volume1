"""Chapter 10, exercise 8: choose the threshold that costs the least.

A missed bad loan (false negative) costs £5,000. Reviewing a good loan by mistake (false positive) costs £200.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

loans = pd.read_csv("data/learning/loans_2026.csv")
loans["income_k"] = loans.annual_income / 1000
features = ["credit_score", "ltv_original_pct", "income_k", "used", "north_west"]
train, test = loans[loans.set == "train"], loans[loans.set == "test"]
p = LogisticRegression(C=np.inf, max_iter=100000, tol=1e-10).fit(train[features], train.bad) \
    .predict_proba(test[features])[:, 1]
actual = test.bad.to_numpy() == 1
for th in (0.50, 0.20, 0.10, 0.05, 0.02):
    flagged = p >= th
    fp, fn = int((flagged & ~actual).sum()), int((~flagged & actual).sum())
    print(f"threshold {th:.2f}: FP={fp:4d} FN={fn:2d}  cost = {fp} x 200 + {fn} x 5,000 = £{fp * 200 + fn * 5000:,}")
