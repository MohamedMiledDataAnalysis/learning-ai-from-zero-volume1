"""Volume 1 Part III: the figures quoted in chapters 13-20 come from these scripts."""

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


def run(cmd):
    if cmd[0] == "python":
        cmd = [sys.executable] + cmd[1:]
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stderr
    return r.stdout


@pytest.mark.parametrize("cmd, expected", [
    (["python", "python/vol1/ch13/eligibility_rules.py"],
     ["Rows passing all six rules: 5001", "TAR00888: R1 borrower resident in the UK"]),
    (["Rscript", "r/vol1/ch13/eligibility_rules.R"], ["Rows passing all six rules: 5001", "TAR00888"]),
    (["python", "python/vol1/ch13/expert_system.py"],
     ["step 3: affordability_problem  =>  offer_payment_plan", "step 4: ninety_days_in_arrears"]),
    (["python", "python/vol1/ch14/convolution_by_hand.py"], ["Sum = 27", "[ 27  27 -27]"]),
    (["python", "python/vol1/ch14/digits_classifier.py"],
     ["Images: 1797", "test images: 450", "Accuracy on the test images: 97.3%"]),
    (["python", "python/vol1/ch15/tiny_rnn.py"],
     ["epoch 3000: 0.0073", "Mean absolute error: RNN 0.095 | naive 0.118"]),
    (["python", "python/vol1/ch16/markov_text.py"],
     ["9,662 characters, 72 different characters", "'h' (158)", "Order 6: Important notice This document"]),
    (["python", "python/vol1/ch16/neural_bigram.py"], ["Loss if every character is equally likely: 4.277",
                                                        "step 300: loss 2.388"]),
    (["python", "python/vol1/ch16/copy_check.py"],
     ["Order 3: 0 of 91 windows", "Order 6: 48 of 91 windows"]),
    (["python", "python/vol1/ch17/diffusion_2d.py"],
     ["start (pure noise): 0.534", "after reverse step 40: 0.038", "within 0.15 of the circle: 100%"]),
    (["python", "python/vol1/ch18/spectrogram.py"],
     ["frequency step: 20 Hz", "10 |   0.50 s  | 660 Hz", "[0.0, 0.0, 4.0, 0.0, 0.0]"]),
    (["python", "python/vol1/ch19/collections_q_learning.py"],
     ["1 in arrears   |     56.6 |     67.3 |     56.1 | reminder",
      "3 in arrears   |   -193.3 |   -175.3 |   -112.9 | call"]),
    (["python", "python/vol1/ch20/recommender.py"], ["Amira  0.816", "Tyre cover         1.316"]),
    (["python", "python/vol1/ch20/forecast_pool.py"],
     ["balance = 74.163 + (-2.512 x period)", "straight line: 0.295 £m", "naive        : 4.673 £m"]),
    (["Rscript", "r/vol1/ch20/forecast_pool.R"], ["Period 12: forecast 44.01, actual 44.58"]),
])
def test_script_output(cmd, expected):
    out = run(cmd)
    for line in expected:
        assert line in out, line


def test_part3_check_scripts_accept_correct_answers():
    for n in range(13, 21):
        out = run(["python", f"python/vol1/ch{n}/check_ch{n}.py", "--demo"])
        assert "PASS" in out, n
