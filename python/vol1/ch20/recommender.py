"""Chapter 20 — a recommender built on similarity.

ILLUSTRATIVE DATA: the purchase table below is invented for this chapter.
Rows are customers of the car finance company, columns are add-on products;
1 means the customer bought it.
"""

import numpy as np

PRODUCTS = ["GAP insurance", "Service plan", "Tyre cover", "Extended warranty"]
CUSTOMERS = ["Amira", "Ben", "Chloe", "Dev", "Ella"]
bought = np.array([
    [1, 1, 0, 1],    # Amira
    [1, 1, 1, 0],    # Ben
    [0, 0, 1, 0],    # Chloe
    [1, 1, 0, 0],    # Dev  <- we recommend for Dev
    [0, 1, 1, 0],    # Ella
])


def cosine(a, b):
    """1 = identical tastes, 0 = nothing in common."""
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


target = CUSTOMERS.index("Dev")
print("Similarity of Dev to each other customer:")
sims = {}
for i, name in enumerate(CUSTOMERS):
    if i != target:
        sims[name] = cosine(bought[target], bought[i])
        print(f"  {name:<6} {sims[name]:.3f}")

# Score each product Dev does not have: add up the similarities of the customers who bought it.
print("\nScores for the products Dev has not bought:")
for j, product in enumerate(PRODUCTS):
    if bought[target, j] == 0:
        score = sum(sims[name] * bought[CUSTOMERS.index(name), j] for name in sims)
        print(f"  {product:<18} {score:.3f}")
