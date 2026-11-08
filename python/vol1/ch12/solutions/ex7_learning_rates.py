"""Chapter 12, exercise 7: the same network trained with three learning rates."""

import json
from pathlib import Path

import numpy as np
import pandas as pd

loans = pd.read_csv("data/learning/loans_2026.csv")
loans["income_k"] = loans.annual_income / 1000
FEATURES = ["credit_score", "ltv_original_pct", "income_k", "north_west"]
train = loans[loans.set == "train"]
X = ((train[FEATURES] - train[FEATURES].mean()) / train[FEATURES].std(ddof=0)).to_numpy()
y = train.bad.to_numpy().reshape(-1, 1)
start = json.loads(Path("data/learning/nn_initial_weights.json").read_text(encoding="utf-8"))
sigmoid = lambda z: 1 / (1 + np.exp(-z))  # noqa: E731

for lr in (0.3, 1.0, 10.0):
    W1, b1, W2, b2 = (np.array(start[k], dtype=float) for k in ("W1", "b1", "W2", "b2"))
    losses = {}
    for epoch in range(3001):
        H = sigmoid(X @ W1 + b1); P = sigmoid(H @ W2 + b2)
        if epoch in (10, 100, 3000):
            losses[epoch] = float(-(y * np.log(P) + (1 - y) * np.log(1 - P)).mean())
        d2 = (P - y) / len(X); d1 = (d2 @ W2.T) * H * (1 - H)
        W2 -= lr * H.T @ d2; b2 -= lr * d2.sum(0); W1 -= lr * X.T @ d1; b1 -= lr * d1.sum(0)
    print(f"learning rate {lr:5.1f}: loss at epoch 10 = {losses[10]:.5f}, 100 = {losses[100]:.5f}, "
          f"3000 = {losses[3000]:.5f}")
