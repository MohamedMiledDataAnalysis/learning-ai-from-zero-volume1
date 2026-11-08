"""Chapter 9: fit a straight line through 5 loans, step by step, as you would on paper."""

import pandas as pd

loans = pd.read_csv("data/learning/loans_2026.csv")
# The first 5 new-car loans in the training set.
five = loans[(loans.used == 0) & (loans.set == "train")].head(5)
x = five.credit_score.to_numpy()          # input: credit score
y = five.interest_rate_pct.to_numpy()     # output: interest rate in percent

x_mean, y_mean = x.mean(), y.mean()
print(f"Step 1  mean score = {x_mean:.1f}   mean rate = {y_mean:.3f}")

print("Step 2  deviations from the means")
print("  loan       score  rate   dx       dy       dx*dy      dx*dx")
for lid, xi, yi in zip(five.loan_id, x, y):
    dx, dy = xi - x_mean, yi - y_mean
    print(f"  {lid}  {xi:5d}  {yi:5.2f}  {dx:7.1f}  {dy:7.3f}  {dx * dy:9.3f}  {dx * dx:9.2f}")
sxy = ((x - x_mean) * (y - y_mean)).sum()
sxx = ((x - x_mean) ** 2).sum()
print(f"  totals                              {sxy:9.3f}  {sxx:9.2f}")

slope = sxy / sxx
intercept = y_mean - slope * x_mean
print(f"Step 3  slope = {sxy:.3f} / {sxx:.2f} = {slope:.5f}")
print(f"Step 4  intercept = {y_mean:.3f} - ({slope:.5f} x {x_mean:.1f}) = {intercept:.3f}")
print(f"Step 5  predicted rate for a score of 700 = {intercept:.3f} + ({slope:.5f} x 700) = "
      f"{intercept + slope * 700:.2f}%")
