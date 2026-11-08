"""Chapter 5 — practical task: how many loans in the received tape are PCP loans?

Count it in a spreadsheet (filter the column `product`), then run:

    python python/vol1/ch05/check_ch05.py 1234
"""

import sys

import pandas as pd

tape = pd.read_csv("data/loan_tape_cutoff.csv")
correct = int((tape["product"] == "PCP").sum())
if len(sys.argv) != 2 or not sys.argv[1].replace(",", "").isdigit():
    print("Give your answer as a whole number, for example: python python/vol1/ch05/check_ch05.py 1234")
elif int(sys.argv[1].replace(",", "")) == correct:
    print(f"Correct: {correct:,} rows of the received tape are PCP loans.")
else:
    print("Not quite. Check that you counted rows where `product` is exactly PCP, in the whole file "
          "(all 5,002 rows). Reread Section 5.3.")
