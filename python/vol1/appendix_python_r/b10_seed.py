# B.10 Random numbers and the seed.
import numpy as np

rng = np.random.default_rng(seed=42)
print(rng.integers(1, 7, size=5))   # five dice
rng = np.random.default_rng(seed=42)
print(rng.integers(1, 7, size=5))   # same five
