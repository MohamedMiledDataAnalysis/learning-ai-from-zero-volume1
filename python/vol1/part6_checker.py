"""Shared helper for the practical tasks of Part VI: compares your answer with the computed one."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE / "ch29"), str(HERE / "ch31"), str(HERE / "ch32"), str(HERE / "ch33"), str(HERE.parent)]


def grade(task, expected, section, tolerance=0.005):
    if len(sys.argv) < 2:
        print(f"Usage: give your answer after the command, for example: ... {sys.argv[0]} 12")
        sys.exit(1)
    try:
        given = float(sys.argv[1].replace("€", "").replace("£", ""))
    except ValueError:
        print("Your answer must be a number.")
        sys.exit(1)
    if abs(given - expected) <= tolerance:
        print(f"Correct: {task} = {sys.argv[1]}. 1 point.")
    else:
        print(f"Not yet: {sys.argv[1]} is not right. Reread {section} and run the steps again.")
