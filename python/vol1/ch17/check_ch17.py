"""Practical task (chapter 17): with the chapter's noise schedule, what share of the original signal
is left after all 40 steps? This is the square root of alpha_bar at step 40. Answer with 3 decimals."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from part3_checker import check

alpha_bar = np.cumprod(1 - np.linspace(1e-4, 0.08, 40))
check(round(float(np.sqrt(alpha_bar[-1])), 3), 0.0015, "§ 17.4")
