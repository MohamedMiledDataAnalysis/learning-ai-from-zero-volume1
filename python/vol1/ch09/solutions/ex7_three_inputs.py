"""Chapter 9, exercise 7: add a third input (PCP or HP) and compare the test error."""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

loans = pd.read_csv("data/learning/loans_2026.csv")
train, test = loans[loans.set == "train"], loans[loans.set == "test"]
for cols in (["credit_score", "used"], ["credit_score", "used", "pcp"]):
    m = LinearRegression().fit(train[cols], train.interest_rate_pct)
    rmse = np.sqrt(((test.interest_rate_pct - m.predict(test[cols])) ** 2).mean())
    coefs = "  ".join(f"{c}={v:.4f}" for c, v in zip(cols, m.coef_))
    print(f"{' + '.join(cols):30s} test RMSE = {rmse:.4f}   {coefs}")
