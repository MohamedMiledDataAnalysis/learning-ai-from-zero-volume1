"""Chapter 20 — forecast the pool balance for October to December 2026.

We pretend today is the end of September (period 9): we know periods 1-9 and
forecast periods 10-12. Then we compare with what really happened.
"""

import json
from pathlib import Path

import numpy as np

files = sorted(Path("data/investor_reports").glob("investor_report_2026_*.json"))
balance = np.array([json.loads(f.read_text(encoding="utf-8"))["pool"]["closing_balance"] for f in files]) / 1e6   # £m
known, actual = balance[:9], balance[9:]
months = np.arange(1, 13)

# Method 1 - naive: the balance stays where it is.
naive = np.repeat(known[-1], 3)
# Method 2 - average fall: continue the average monthly fall of the last 3 months.
avg_fall = np.mean(np.diff(known)[-3:])
moving = known[-1] + avg_fall * np.arange(1, 4)
# Method 3 - straight line (linear regression) through the 9 known months.
slope, intercept = np.polyfit(months[:9], known, 1)
trend = intercept + slope * months[9:]

print("Known closing balances, periods 1-9 (£m):", " ".join(f"{v:.2f}" for v in known))
print(f"Average fall over periods 7-9: {avg_fall:.3f} £m per month")
print(f"Straight line: balance = {intercept:.3f} + ({slope:.3f} x period)")
print("\nperiod | actual | naive | average fall | straight line")
for k in range(3):
    print(f"{10 + k:>6} | {actual[k]:6.2f} | {naive[k]:5.2f} | {moving[k]:12.2f} | {trend[k]:13.2f}")
for name, f in [("naive", naive), ("average fall", moving), ("straight line", trend)]:
    print(f"Mean absolute error, {name:<13}: {np.mean(np.abs(f - actual)):.3f} £m")
