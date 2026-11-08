"""Check your answer to the practical task of chapter 9.

Task: fit rate = a + b x credit_score on the USED cars of the training set only.
Run:  python python/vol1/ch09/check_ch09.py --slope -0.0120
"""

import argparse

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--slope", type=float, required=True, help="your slope b, 4 decimal places")
answer = parser.parse_args().slope

loans = pd.read_csv("data/learning/loans_2026.csv")
used = loans[(loans.set == "train") & (loans.used == 1)]
slope = np.polyfit(used.credit_score, used.interest_rate_pct, 1)[0]
if abs(answer - round(slope, 4)) < 0.00005:
    print(f"Correct: the slope is {slope:.4f}.")
else:
    print("Not yet. Check that you kept only used cars AND only the training set, then reread section 9.4.")
