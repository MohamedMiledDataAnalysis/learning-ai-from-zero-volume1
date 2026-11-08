"""Shared helper for the Part III practical-task checkers.

Usage from the repository root:  python python/vol1/chNN/check_chNN.py <your answer>
                                 python python/vol1/chNN/check_chNN.py --demo   (shows a correct answer)
"""

import sys


def check(expected, tolerance, section, unit=""):
    if len(sys.argv) < 2:
        print("Give your answer after the command, for example: python python/vol1/ch13/check_ch13.py 4321")
        return
    if sys.argv[1] == "--demo":
        answer = expected
    else:
        try:
            answer = float(sys.argv[1].replace(",", "").replace("£", "").replace("%", ""))
        except ValueError:
            answer = sys.argv[1]
    if isinstance(answer, str) or isinstance(expected, str):
        ok = str(answer).strip().lower() == str(expected).strip().lower()
    else:
        ok = abs(answer - expected) <= tolerance
    if ok:
        print(f"PASS - your answer {answer}{unit} is correct.")
    else:
        print(f"FAIL - {answer}{unit} is not the expected value. Reread {section} and run the steps again.")
