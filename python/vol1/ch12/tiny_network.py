"""Chapter 12: a network with 4 inputs, 3 hidden neurons and 1 output, written with numpy only."""

import json
from pathlib import Path

import numpy as np
import pandas as pd

loans = pd.read_csv("data/learning/loans_2026.csv")
loans["income_k"] = loans.annual_income / 1000
FEATURES = ["credit_score", "ltv_original_pct", "income_k", "north_west"]
train, test = loans[loans.set == "train"], loans[loans.set == "test"]

# Scale with the training set's mean and (population) standard deviation, then apply the same to the test set.
mean, sd = train[FEATURES].mean().to_numpy(), train[FEATURES].std(ddof=0).to_numpy()
X_train, X_test = (train[FEATURES].to_numpy() - mean) / sd, (test[FEATURES].to_numpy() - mean) / sd
y_train = train.bad.to_numpy().reshape(-1, 1)

start = json.loads(Path("data/learning/nn_initial_weights.json").read_text(encoding="utf-8"))
W1, b1 = np.array(start["W1"]), np.array(start["b1"])      # 4 x 3 and 3
W2, b2 = np.array(start["W2"]), np.array(start["b2"])      # 3 x 1 and 1


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def forward(X):
    H = sigmoid(X @ W1 + b1)          # hidden layer: 3 numbers per loan
    P = sigmoid(H @ W2 + b2)          # output: probability of going bad
    return H, P


def loss(P, y):
    return float(-(y * np.log(P) + (1 - y) * np.log(1 - P)).mean())


LR, EPOCHS = 1.0, 3000
n = len(X_train)
print("epoch   training loss")
for epoch in range(EPOCHS + 1):
    H, P = forward(X_train)
    if epoch in (0, 1, 10, 100, 500, 1000, 2000, 3000):
        print(f"{epoch:5d}   {loss(P, y_train):.5f}")
    # Backward pass: how much each weight contributed to the error (averaged over all loans).
    dZ2 = (P - y_train) / n
    dW2, db2 = H.T @ dZ2, dZ2.sum(axis=0)
    dZ1 = (dZ2 @ W2.T) * H * (1 - H)
    dW1, db1 = X_train.T @ dZ1, dZ1.sum(axis=0)
    # Gradient descent: a small step against the gradient.
    W1 -= LR * dW1; b1 -= LR * db1; W2 -= LR * dW2; b2 -= LR * db2

_, P_test = forward(X_test)
p = P_test.ravel()
actual = test.bad.to_numpy() == 1
for th in (0.50, 0.10):
    flagged = p >= th
    tp, fp = int((flagged & actual).sum()), int((flagged & ~actual).sum())
    fn = int((~flagged & actual).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    print(f"Test, threshold {th:.2f}: TP={tp} FP={fp} FN={fn}  precision={precision:.2%}  recall={tp / (tp + fn):.2%}")
print("Output weights W2: [" + ", ".join(f"{w:.4f}" for w in W2.ravel()) + "]")
