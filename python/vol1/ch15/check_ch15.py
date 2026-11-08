"""Practical task (chapter 15): forecast months 11 and 12 with the average of the two previous
months' prepayments (in £m). Give the mean absolute error in £m, three decimals."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from part3_checker import check
from ch15.tiny_rnn import load_prepayments

p = load_prepayments()
errors = [abs(p[m - 3:m - 1].mean() - p[m - 1]) for m in (11, 12)]
check(round(float(np.mean(errors)), 3), 0.0015, "§ 15.2")
