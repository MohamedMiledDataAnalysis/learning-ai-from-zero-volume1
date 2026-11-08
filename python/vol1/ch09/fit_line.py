"""Chapter 9: linear regression on the whole training set, then tested on loans it has never seen."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")                     # draw charts to a file, no window
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

loans = pd.read_csv("data/learning/loans_2026.csv")
train, test = loans[loans.set == "train"], loans[loans.set == "test"]


def evaluate(model, columns):
    """Error measures on the test set: loans the model did not learn from."""
    predicted = model.predict(test[columns])
    errors = test.interest_rate_pct - predicted
    rmse = np.sqrt((errors ** 2).mean())
    r2 = 1 - (errors ** 2).sum() / ((test.interest_rate_pct - test.interest_rate_pct.mean()) ** 2).sum()
    return rmse, r2


# Model 1: one input, the credit score.
m1 = LinearRegression().fit(train[["credit_score"]], train.interest_rate_pct)
rmse1, r21 = evaluate(m1, ["credit_score"])
print("Model 1: rate = a + b x score")
print(f"  intercept a = {m1.intercept_:.4f}   slope b = {m1.coef_[0]:.6f}")
print(f"  test RMSE = {rmse1:.3f} points   test R-squared = {r21:.3f}")

# Model 2: two inputs, the credit score and whether the car is used (1) or new (0).
cols = ["credit_score", "used"]
m2 = LinearRegression().fit(train[cols], train.interest_rate_pct)
rmse2, r22 = evaluate(m2, cols)
print("Model 2: rate = a + b x score + c x used")
print(f"  intercept a = {m2.intercept_:.4f}   b = {m2.coef_[0]:.6f}   c = {m2.coef_[1]:.4f}")
print(f"  test RMSE = {rmse2:.3f} points   test R-squared = {r22:.3f}")

new_loan = pd.DataFrame({"credit_score": [700], "used": [1]})
print(f"Prediction for a used car, score 700: {m2.predict(new_loan)[0]:.2f}%")

# Chart: 400 training loans and the two lines of model 2.
sample = train.sample(400, random_state=1)
fig, ax = plt.subplots(figsize=(4.4, 2.9))
for used, colour, label in [(0, "#1F2F54", "New car"), (1, "#B8892B", "Used car")]:
    s = sample[sample.used == used]
    ax.scatter(s.credit_score, s.interest_rate_pct, s=7, alpha=0.6, color=colour, label=label)
    xs = np.array([500, 999])
    ax.plot(xs, m2.intercept_ + m2.coef_[0] * xs + m2.coef_[1] * used, color=colour, linewidth=1.6)
ax.set_xlabel("Credit score")
ax.set_ylabel("Interest rate (%)")
ax.legend(frameon=False, fontsize=8)
fig.tight_layout()
out = Path("book/figures/build") if Path("book").is_dir() else Path("output/figures")
out.mkdir(parents=True, exist_ok=True)
fig.savefig(out / "v1-ch09-scatter.pdf")
fig.savefig(out / "v1-ch09-scatter.png", dpi=200)
