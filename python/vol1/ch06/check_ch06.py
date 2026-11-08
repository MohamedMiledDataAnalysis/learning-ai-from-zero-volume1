"""Chapter 6 — practical task: the mean squared error of the guess a = 18, b = -1.1 on the six loans.

Compute it by hand (round every number to 2 decimals, as in Section 6.4), then run:

    python python/vol1/ch06/check_ch06.py 1.23
"""

import sys

CORRECT = 0.78     # printed by python/vol1/ch06/tiny_model.py, checked by the tests
try:
    answer = float(sys.argv[1])
except (IndexError, ValueError):
    raise SystemExit("Give your answer as a number, for example: python python/vol1/ch06/check_ch06.py 1.23")
if abs(answer - CORRECT) < 0.005:
    print("Correct: the mean squared error is 0.78.")
elif abs(answer - 4.65) < 0.005:
    print("You found the sum of the squared errors (4.65). Divide it by the number of loans, 6. Reread Section 6.4.")
elif abs(answer - 0.99) < 0.005:
    print("That is the error of the first guess (a = 20, b = -1.4). Use a = 18 and b = -1.1. Reread Section 6.4.")
else:
    print("Not quite. For each loan: prediction = 18 - 1.1 x (score / 100), error = rate - prediction, square it; "
          "then average the six squares. Reread Section 6.4.")
