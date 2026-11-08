"""Chapter 10, exercise 7: what happens to the logistic regression without the North West indicator?"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

loans = pd.read_csv("data/learning/loans_2026.csv")
loans["income_k"] = loans.annual_income / 1000
train, test = loans[loans.set == "train"], loans[loans.set == "test"]
actual = test.bad.to_numpy() == 1

for features in (["credit_score", "ltv_original_pct", "income_k", "used", "north_west"],
                 ["credit_score", "ltv_original_pct", "income_k", "used"]):
    m = LogisticRegression(C=np.inf, max_iter=100000, tol=1e-10).fit(train[features], train.bad)
    flagged = m.predict_proba(test[features])[:, 1] >= 0.10
    tp, fp = int((flagged & actual).sum()), int((flagged & ~actual).sum())
    label = "with north_west" if "north_west" in features else "without north_west"
    print(f"{label:20s} threshold 0.10: TP={tp:2d} FP={fp:3d}  recall={tp / actual.sum():.2%}")
