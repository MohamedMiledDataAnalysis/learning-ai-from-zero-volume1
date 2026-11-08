"""Chapter 8 — practical task: the precision of Rule 2 ("borrower in the North West"), in %, two decimals.

From the confusion matrix printed in Section 8.5 (TP 99, FP 476), compute it, then run:

    python python/vol1/ch08/check_ch08.py 12.34
"""

import sys

TP, FP, FN = 99, 476, 47           # printed by python/vol1/ch08/judge_rules.py, checked by the tests
precision, recall = 100 * TP / (TP + FP), 100 * TP / (TP + FN)
try:
    answer = float(sys.argv[1].rstrip("%"))
except (IndexError, ValueError):
    raise SystemExit("Give your answer in %, for example: python python/vol1/ch08/check_ch08.py 12.34")
if abs(answer - round(precision, 2)) < 0.006:
    print(f"Correct: precision = 99 / (99 + 476) = {precision:.2f}%.")
elif abs(answer - round(recall, 2)) < 0.006:
    print("That is the recall (TP / (TP + FN)). Precision divides by all loans predicted bad: TP + FP. "
          "Reread Section 8.5.")
else:
    print("Not quite. Precision = TP / (TP + FP): of the loans the rule calls bad, the share that really were. "
          "Reread Section 8.5.")
