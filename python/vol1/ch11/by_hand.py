"""Chapter 11: two rounds of k-means on six points, printing every distance."""

import numpy as np

points = {"A": (-1.0, 0.5), "B": (-1.2, -0.3), "C": (0.8, 1.1), "D": (1.1, 0.9), "E": (0.2, -1.0), "F": (1.4, -0.2)}
centres = [np.array(points["A"]), np.array(points["C"])]       # start: the centres sit on A and C

for round_number in (1, 2):
    print(f"Round {round_number}: centres " + "  ".join(f"({c[0]:.3f}, {c[1]:.3f})" for c in centres))
    groups = {0: [], 1: []}
    for name, p in points.items():
        d = [float(np.sqrt(((np.array(p) - c) ** 2).sum())) for c in centres]
        nearest = int(np.argmin(d))
        groups[nearest].append(name)
        print(f"  {name}: distance to centre 1 = {d[0]:.3f}, to centre 2 = {d[1]:.3f} -> group {nearest + 1}")
    centres = [np.mean([points[n] for n in groups[g]], axis=0) for g in (0, 1)]
    print(f"  groups: 1 = {', '.join(groups[0])}, 2 = {', '.join(groups[1])}")
