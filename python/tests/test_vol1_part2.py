"""Volume 1, Part II: the figures quoted in chapters 9 to 12, and Python/R agreement."""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


def run(*cmd):
    if cmd[0] == "python":
        cmd = (sys.executable, *cmd[1:])
    return subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, check=True).stdout


def test_dataset_counts():
    out = run("python", "python/datasets/build_loans_learning.py")
    assert "loans: 4,999  bad: 146 (2.92%)" in out
    assert "train: 3,499 loans, 102 bad   test: 1,500 loans, 44 bad" in out


@pytest.mark.parametrize("script, expected", [
    ("python/vol1/ch09/by_hand.py", ["slope = -739.842 / 39097.20 = -0.01892", "= 10.00%"]),
    ("python/vol1/ch09/fit_line.py", ["slope b = -0.011916", "c = 1.0336", "test R-squared = 0.785",
                                      "score 700: 10.88%"]),
    ("python/vol1/ch10/predict_default.py", ["accuracy 97.07%", "north_west           2.8704   odds x 17.643",
                                             "Logistic, threshold 0.10: TP=29 FP=100 FN=15",
                                             "Tree, threshold 0.10: TP=28 FP=140 FN=16"]),
    ("python/vol1/ch11/segments.py", ["8335.2", "1434.7", "  2   1000    670    38148  11.16"]),
    ("python/vol1/ch12/one_neuron.py", ["p = sigmoid(z) = 1 / (1 + e^-z) = 0.4750", "After     p = 0.6906"]),
    ("python/vol1/ch12/tiny_network.py", [" 3000   0.10217", "TP=30 FP=103 FN=14  precision=22.56%  recall=68.18%"]),
])
def test_quoted_figures(script, expected):
    out = run("python", script)
    for e in expected:
        assert e in out


@pytest.mark.skipif(shutil.which("Rscript") is None, reason="R not installed")
@pytest.mark.parametrize("py, r, lines", [
    ("python/vol1/ch09/fit_line.py", "r/vol1/ch09/fit_line.R", None),
    ("python/vol1/ch10/predict_default.py", "r/vol1/ch10/predict_default.R", "threshold"),
    ("python/vol1/ch11/segments.py", "r/vol1/ch11/segments.R", "  "),
    ("python/vol1/ch12/tiny_network.py", "r/vol1/ch12/tiny_network.R", None),
])
def test_python_and_r_agree(py, r, lines):
    a, b = run("python", py), run("Rscript", r)
    if lines is None:
        assert a == b
    elif lines == "threshold":
        assert [l for l in a.splitlines() if "threshold" in l] == [l for l in b.splitlines() if "threshold" in l]
    else:
        seg = lambda t: [l for l in t.splitlines() if l[:5].strip().isdigit() and "%" in l]  # noqa: E731
        assert seg(a) == seg(b)
