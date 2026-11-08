"""Chapter 22, question 10. Usage: python python/vol1/ch22/check_ch22.py <weight keep->rising> <first number of keep's output>"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from part45_common import grade  # noqa: E402
s = np.array([1.0, 1.0, 2.0]) / np.sqrt(2)            # row 'keep' of the scores
w = np.exp(s) / np.exp(s).sum()
v = np.array([[2.0, 0.0], [0.0, 1.0], [2.0, 1.0]])
grade(sys.argv[1:], [("10a", round(float(w[2]), 3), 0.0015, "22.4"), ("10b", round(float((w @ v)[0]), 3), 0.0015, "22.4")])
