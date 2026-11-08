"""Chapter 23, question 10. Usage: python python/vol1/ch23/check_ch23.py <P(exceed) at t=0.5> <P(sparkle) at t=0.5>"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from part45_common import grade  # noqa: E402
p = np.array([0.62, 0.15, 0.10, 0.08, 0.05]) ** 2       # temperature 0.5 squares the probabilities
p = p / p.sum()
grade(sys.argv[1:], [("10a", round(float(p[0]), 3), 0.0015, "23.4"), ("10b", round(float(p[4]), 3), 0.0015, "23.4")])
