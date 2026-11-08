"""Chapter 11, exercise 7: k-means with k = 5 on the raw columns, without scaling."""

import pandas as pd
from sklearn.cluster import KMeans

loans = pd.read_csv("data/learning/loans_2026.csv")
COLUMNS = ["credit_score", "annual_income", "interest_rate_pct", "original_balance"]
X = loans[COLUMNS].to_numpy()
start = pd.read_csv("data/learning/kmeans_start_rows.csv").row.to_numpy() - 1
print("standard deviations:", "  ".join(f"{c}={X[:, i].std():,.2f}" for i, c in enumerate(COLUMNS)))
model = KMeans(n_clusters=5, init=X[start[:5]], n_init=1, algorithm="lloyd", max_iter=300, tol=0).fit(X)
loans["segment"] = model.labels_ + 1
s = loans.groupby("segment").agg(loans=("loan_id", "count"), score=("credit_score", "mean"),
                                 income=("annual_income", "mean"), balance=("original_balance", "mean"),
                                 bad_rate=("bad", "mean"))
print("seg  loans  score   income   balance  bad rate")
for seg, r in s.iterrows():
    print(f"{seg:3d}  {r.loans:5.0f}  {r.score:5.0f}  {r.income:7.0f}  {r.balance:8.0f}  {r.bad_rate:7.2%}")
