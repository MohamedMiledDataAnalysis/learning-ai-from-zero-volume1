"""Chapter 17 — a diffusion model on 2D points.

The 'images' here are points (x, y) lying on a circle of radius 1. A diffusion model:
  1. Forward: add a little noise, step after step, until the circle becomes a cloud.
  2. Train: a small neural network learns to predict the noise that was added.
  3. Generate: start from pure noise and remove the predicted noise step by step.
If it works, the new points land back on a circle the model was never given as a formula.
"""

import numpy as np
from sklearn.neural_network import MLPRegressor

rng = np.random.default_rng(0)
T = 40                                             # number of noising steps
betas = np.linspace(1e-4, 0.08, T)                 # how much noise each step adds
alphas = 1 - betas
alpha_bar = np.cumprod(alphas)                     # share of the original signal left after t steps

# The training data: 2,000 points on the unit circle.
angles = rng.uniform(0, 2 * np.pi, 2000)
data = np.column_stack([np.cos(angles), np.sin(angles)])


def distance_to_circle(points):
    """Average distance between each point and the circle of radius 1."""
    return float(np.abs(np.linalg.norm(points, axis=1) - 1).mean())


# 1. Forward process: noisy versions of the data at random steps t.
reps = 10
x0 = np.repeat(data, reps, axis=0)
t = rng.integers(0, T, len(x0))
noise = rng.normal(size=x0.shape)
xt = np.sqrt(alpha_bar[t])[:, None] * x0 + np.sqrt(1 - alpha_bar[t])[:, None] * noise
print("Distance to the circle after the forward process:")
for step in (0, 10, 20, 39):
    sel = t == step
    print(f"  step {step + 1:>2}: {distance_to_circle(xt[sel]):.3f}")

# 2. Train the noise predictor: input (x, y, step), output the noise that was added.
features = np.column_stack([xt, t / T])
model = MLPRegressor(hidden_layer_sizes=(64, 64), max_iter=200, random_state=0)
model.fit(features, noise)
print(f"\nNoise predictor trained on {len(features):,} noisy points")

# 3. Generate: start from pure noise and walk the steps backwards.
x = rng.normal(size=(500, 2))
print("\nGeneration (500 new points), distance to the circle:")
print(f"  start (pure noise): {distance_to_circle(x):.3f}")
for step in reversed(range(T)):
    eps = model.predict(np.column_stack([x, np.full(len(x), step / T)]))
    x = (x - betas[step] / np.sqrt(1 - alpha_bar[step]) * eps) / np.sqrt(alphas[step])
    if step > 0:
        x += np.sqrt(betas[step]) * rng.normal(size=x.shape)
    if step in (30, 20, 10, 0):
        print(f"  after reverse step {T - step:>2}: {distance_to_circle(x):.3f}")
inside = float((np.abs(np.linalg.norm(x, axis=1) - 1) < 0.15).mean())
print(f"Share of new points within 0.15 of the circle: {inside:.0%}")
