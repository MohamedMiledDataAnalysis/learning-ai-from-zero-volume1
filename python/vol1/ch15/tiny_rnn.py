"""Chapter 15 — a tiny recurrent neural network (RNN) in numpy.

Task: read the monthly prepayments of the deal one month at a time and predict
next month's prepayments. The RNN keeps a small 'memory' (the hidden state h)
that it updates after every month.

    h_t = tanh(Wx * x_t + Wh @ h_(t-1) + b)      update the memory
    y_t = Wy @ h_t + c                           predict month t+1
"""

import json
from pathlib import Path

import numpy as np

H = 3                  # size of the memory
LEARNING_RATE = 0.05
EPOCHS = 3000


def load_prepayments():
    files = sorted(Path("data/investor_reports").glob("investor_report_2026_*.json"))
    return np.array([json.loads(f.read_text(encoding="utf-8"))["pool"]["prepayments"] for f in files]) / 1e6   # in £ millions


def forward(params, xs):
    Wx, Wh, b, Wy, c = params
    h = np.zeros(H)
    hs, ys = [h], []
    for x in xs:
        h = np.tanh(Wx * x + Wh @ h + b)
        hs.append(h)
        ys.append(float(Wy @ h + c))
    return hs, ys


def train(xs, targets, seed=0):
    rng = np.random.default_rng(seed)
    params = [rng.normal(0, 0.5, H), rng.normal(0, 0.5, (H, H)), np.zeros(H), rng.normal(0, 0.5, H), 0.0]
    history = []
    for epoch in range(EPOCHS + 1):
        Wx, Wh, b, Wy, c = params
        hs, ys = forward(params, xs)
        errors = np.array(ys) - targets
        loss = float((errors ** 2).mean())
        if epoch in (0, 100, 500, 1000, 3000):
            history.append((epoch, loss))
        # Backpropagation through time: walk the sequence backwards, passing the gradient along the memory.
        gWx, gWh, gb, gWy, gc = np.zeros(H), np.zeros((H, H)), np.zeros(H), np.zeros(H), 0.0
        gh_next = np.zeros(H)
        for t in reversed(range(len(xs))):
            dy = 2 * errors[t] / len(xs)
            gWy += dy * hs[t + 1]
            gc += dy
            gh = dy * Wy + gh_next
            gz = gh * (1 - hs[t + 1] ** 2)          # derivative of tanh
            gWx += gz * xs[t]
            gWh += np.outer(gz, hs[t])
            gb += gz
            gh_next = Wh.T @ gz
        params = [Wx - LEARNING_RATE * gWx, Wh - LEARNING_RATE * gWh, b - LEARNING_RATE * gb,
                  Wy - LEARNING_RATE * gWy, c - LEARNING_RATE * gc]
    return params, history


def main():
    prepay = load_prepayments()
    print("Monthly prepayments (£m):", " ".join(f"{v:.2f}" for v in prepay))
    train_x, train_y = prepay[:9], prepay[1:10]          # months 1-9 predict months 2-10
    params, history = train(train_x, train_y)
    print("\nTraining loss (mean squared error, £m squared):")
    for epoch, loss in history:
        print(f"  epoch {epoch:>4}: {loss:.4f}")

    hs, ys = forward(params, prepay[:11])                # read months 1-11
    print("\nMemory (hidden state) after reading each month:")
    for t in (1, 2, 3, 10, 11):
        print(f"  after month {t:>2}: [{', '.join(f'{v:+.2f}' for v in hs[t])}]")

    print("\nTest: predict months 11 and 12 (never used for training)")
    print("  month | actual | RNN  | naive (same as last month)")
    rnn_err, naive_err = [], []
    for month in (11, 12):
        actual, rnn, naive = prepay[month - 1], ys[month - 2], prepay[month - 2]
        rnn_err.append(abs(rnn - actual))
        naive_err.append(abs(naive - actual))
        print(f"  {month:>5} | {actual:.2f}   | {rnn:.2f} | {naive:.2f}")
    print(f"Mean absolute error: RNN {np.mean(rnn_err):.3f} | naive {np.mean(naive_err):.3f} (£m)")


if __name__ == "__main__":
    main()
