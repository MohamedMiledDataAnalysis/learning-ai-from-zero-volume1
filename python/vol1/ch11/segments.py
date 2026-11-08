"""Chapter 11: group borrowers into segments with k-means."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

loans = pd.read_csv("data/learning/loans_2026.csv")
COLUMNS = ["credit_score", "annual_income", "interest_rate_pct", "original_balance"]
X = loans[COLUMNS].to_numpy()

# Put every column on the same scale: subtract the mean, divide by the standard deviation.
# numpy's std() divides by n (the "population" standard deviation), like scikit-learn's StandardScaler.
Z = (X - X.mean(axis=0)) / X.std(axis=0)

# The starting centres are fixed rows of the data (the same rows in Python and R).
start = pd.read_csv("data/learning/kmeans_start_rows.csv").row.to_numpy() - 1   # R counts from 1

print("k   within-cluster sum of squares   drop")
inertias = {}
for k in range(2, 9):
    model = KMeans(n_clusters=k, init=Z[start[:k]], n_init=1, algorithm="lloyd", max_iter=300, tol=0).fit(Z)
    inertias[k] = model.inertia_
    drop = f"{inertias[k - 1] - inertias[k]:8.1f}" if k > 2 else "       -"
    print(f"{k}   {model.inertia_:10.1f}                   {drop}")

K = 5
model = KMeans(n_clusters=K, init=Z[start[:K]], n_init=1, algorithm="lloyd", max_iter=300, tol=0).fit(Z)
loans["segment"] = model.labels_ + 1
summary = loans.groupby("segment").agg(loans=("loan_id", "count"), score=("credit_score", "mean"),
                                       income=("annual_income", "mean"), rate=("interest_rate_pct", "mean"),
                                       balance=("original_balance", "mean"), bad_rate=("bad", "mean"))
print(f"\nSegments with k = {K} (averages in original units)")
print("seg  loans  score   income   rate   balance  bad rate")
for seg, r in summary.iterrows():
    print(f"{seg:3d}  {r.loans:5.0f}  {r.score:5.0f}  {r.income:7.0f}  {r.rate:5.2f}  {r.balance:8.0f}  {r.bad_rate:7.2%}")

# The elbow chart.
fig, ax = plt.subplots(figsize=(4.2, 2.6))
ax.plot(list(inertias), list(inertias.values()), marker="o", color="#1F2F54")
ax.axvline(K, color="#B8892B", linestyle="--", linewidth=1)
ax.set_xlabel("Number of segments k")
ax.set_ylabel("Within-cluster sum of squares")
fig.tight_layout()
out = Path("book/figures/build") if Path("book").is_dir() else Path("output/figures")
out.mkdir(parents=True, exist_ok=True)
fig.savefig(out / "v1-ch11-elbow.pdf")
fig.savefig(out / "v1-ch11-elbow.png", dpi=200)
