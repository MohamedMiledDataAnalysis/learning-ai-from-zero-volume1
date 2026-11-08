"""Volume 1, Part 0 and Part I: every figure quoted in the text of Chapters 2 to 8.

Run from the python/ folder: python -m pytest -q tests/test_vol1_part1.py
"""

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


def run(script, *args):
    r = subprocess.run([sys.executable, script, *args], cwd=REPO, capture_output=True, text=True, check=True)
    return r.stdout


@pytest.fixture(scope="module")
def ch05():
    return run("python/vol1/ch05/explore_tape.py")


@pytest.fixture(scope="module")
def ch06():
    return run("python/vol1/ch06/tiny_model.py")


@pytest.fixture(scope="module")
def ch08():
    return run("python/vol1/ch08/judge_rules.py")


@pytest.mark.parametrize("text", [
    "Rows: 5,002   Columns: 21", "loan_id                TAR00001", "current_balance        12882.49",
    "monthly_instalment     634.56", "HP   2,037", "PCP  2,965", "Different regions written in the tape: 13",
    "Empty postcode cells: 2", "Rows that are exact copies of another row: 2",
])
def test_chapter5_figures(ch05, text):
    assert text in ch05


@pytest.mark.parametrize("text", [
    "TAR00011  x = 7.10   y = 10.23", "TAR00051  x = 9.78   y =  5.57",
    "TAR00022: prediction  6.85  error  +1.71  squared   2.92",
    "sum of squares = 5.95, divided by 6 = 0.99", "sum of squares = 4.65, divided by 6 = 0.78",
    "Best line for the six loans: a = 20.42, b = -1.39, mean squared error = 0.71",
    "Best line for all 4,998 loans: a = 18.82, b = -1.19, mean squared error = 0.61",
    "Prediction for a score of 700 with the all-loans line: 10.46%",
])
def test_chapter6_figures(ch06, text):
    assert text in ch06


@pytest.mark.parametrize("text", [
    "Reached 90+ days in arrears in 2026: 146 (2.92%)",
    "TP    0  FP    0  FN  146  TN  4854", "accuracy 97.08%",
    "TP   49  FP  844  FN   97  TN  4010", "accuracy 81.18%   precision 5.49%   recall 33.56%",
    "TP   99  FP  476  FN   47  TN  4378", "accuracy 89.54%   precision 17.22%   recall 67.81%",
    "Training set: 3,482 loans (102 went 90+). Test set: 1,518 loans (44 went 90+).",
    "accuracy 100.00%   precision 100.00%   recall 100.00%",
    "TP    0  FP    0  FN   44  TN  1474",
    "accuracy 82.31%   precision 6.29%   recall 36.27%", "accuracy 78.59%   precision 3.93%   recall 27.27%",
    "TP   23  FP  323  FN  123  TN  4531", "accuracy 91.08%   precision 6.65%   recall 15.75%",
])
def test_chapter8_figures(ch08, text):
    assert text in ch08


def test_chapter6_by_hand_solution_6_5():
    """Solution 6.5: the guess a = 19, b = -1.2 gives MSE 0.76 when every number is rounded to 2 decimals."""
    xs = [7.10, 9.39, 9.78, 8.13, 7.96, 8.59]
    ys = [10.23, 8.56, 5.57, 8.49, 9.72, 9.27]
    squares = []
    for x, y in zip(xs, ys):
        e = round(y - round(19 - 1.2 * x, 2), 2)
        squares.append(round(e * e, 2))
    assert round(sum(squares), 2) == 4.58
    assert round(sum(squares) / 6, 2) == 0.76


@pytest.mark.parametrize("script, good, bad", [
    ("python/vol1/ch05/check_ch05.py", "2965", "2000"),
    ("python/vol1/ch06/check_ch06.py", "0.78", "4.65"),
    ("python/vol1/ch08/check_ch08.py", "17.22", "67.81"),
])
def test_check_scripts(script, good, bad):
    assert run(script, good).startswith("Correct")
    assert not run(script, bad).startswith("Correct")


def test_chapter2_environment_check_runs():
    out = run("python/vol1/ch02/check_ch02.py")
    assert "OK       Python package pandas 3.0.5" in out
    assert "file data/loan_tape_cutoff.csv" in out
