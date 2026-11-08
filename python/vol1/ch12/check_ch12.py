"""Check your answer to the practical task of chapter 12.

Task: in tiny_network.py, change the learning rate LR from 1.0 to 0.1 and keep 3000 epochs.
What is the training loss at epoch 3000 (5 decimals)?
Run:  python python/vol1/ch12/check_ch12.py --loss 0.12345
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--loss", type=float, required=True)
answer = parser.parse_args().loss

loans = pd.read_csv("data/learning/loans_2026.csv")
loans["income_k"] = loans.annual_income / 1000
features = ["credit_score", "ltv_original_pct", "income_k", "north_west"]
train = loans[loans.set == "train"]
X = ((train[features] - train[features].mean()) / train[features].std(ddof=0)).to_numpy()
y = train.bad.to_numpy().reshape(-1, 1)
w = json.loads(Path("data/learning/nn_initial_weights.json").read_text(encoding="utf-8"))
W1, b1, W2, b2 = (np.array(w[k]) for k in ("W1", "b1", "W2", "b2"))
s = lambda z: 1 / (1 + np.exp(-z))  # noqa: E731
for _ in range(3001):
    H = s(X @ W1 + b1); P = s(H @ W2 + b2)
    loss = float(-(y * np.log(P) + (1 - y) * np.log(1 - P)).mean())
    d2 = (P - y) / len(X); d1 = (d2 @ W2.T) * H * (1 - H)
    W2 -= 0.1 * H.T @ d2; b2 -= 0.1 * d2.sum(0); W1 -= 0.1 * X.T @ d1; b1 -= 0.1 * d1.sum(0)
if abs(answer - round(loss, 5)) < 0.000005:
    print(f"Correct: the loss at epoch 3000 is {loss:.5f}.")
else:
    print("Not yet. Change only LR, and read the loss printed for epoch 3000. Reread section 12.4.")
