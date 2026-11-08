"""Check your answer to the practical task of chapter 11.

Task: run k-means with k = 4 (same scaling, same starting rows). How many loans are in the largest segment?
Run:  python python/vol1/ch11/check_ch11.py --largest 1500
"""

import argparse

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

parser = argparse.ArgumentParser()
parser.add_argument("--largest", type=int, required=True)
answer = parser.parse_args().largest

loans = pd.read_csv("data/learning/loans_2026.csv")
X = loans[["credit_score", "annual_income", "interest_rate_pct", "original_balance"]].to_numpy()
Z = (X - X.mean(axis=0)) / X.std(axis=0)
start = pd.read_csv("data/learning/kmeans_start_rows.csv").row.to_numpy() - 1
labels = KMeans(n_clusters=4, init=Z[start[:4]], n_init=1, algorithm="lloyd", max_iter=300, tol=0).fit(Z).labels_
largest = int(np.bincount(labels).max())
if answer == largest:
    print(f"Correct: the largest segment has {largest} loans.")
else:
    print("Not yet. Use the first 4 starting rows and the population standard deviation. Reread section 11.3.")
