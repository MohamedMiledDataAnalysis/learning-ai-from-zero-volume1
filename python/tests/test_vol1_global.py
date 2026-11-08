"""Tests for the Volume 1 global assessment and Appendix A: every figure the text quotes."""

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
GA = REPO / "python" / "vol1" / "global_assessment"
# The chapter text is in the manuscript, which is not part of the public companion repository:
# tests that read it are skipped there.
BOOK = REPO / "book" / "vol1"
needs_book = pytest.mark.skipif(not BOOK.is_dir(), reason="manuscript not in this repository")
TEXT = (BOOK / "global-assessment.md").read_text(encoding="utf-8") if BOOK.is_dir() else ""
MATHS = (BOOK / "appendix-maths.md").read_text(encoding="utf-8") if BOOK.is_dir() else ""


def run(*args):
    # No bytecode cache: a file rewritten within the same second could otherwise be run from a stale cache.
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    r = subprocess.run([sys.executable, "-B", *map(str, args)], cwd=REPO, capture_output=True, text=True,
                       check=True, env=env)
    return r.stdout


@pytest.fixture(scope="module")
def part_c():
    return run(GA / "part_c_answers.py")


@pytest.mark.parametrize("figure", [
    "= -0.98", "p = 1 / (1 + e^0.98) = 0.2729", "dw1 = (p - y) x1 = -0.5817", "new w1 = -0.3092, new w2 = 1.8636, "
    "new b = -1.6364", "new p = 0.4949, loss after = 0.7033", "loss before = -ln(0.2729) = 1.2987",
    "TP = 33, FP = 133, FN = 11, TN = 1323", "precision = 33 / (33 + 133) = 0.1988", "recall    = 33 / (33 + 11) = 0.7500",
    "weight = 0.1978", "weight = 0.4011", "sum of e^score = 10.2546", "tokens (18)", "-> £1.80",
])
def test_part_c_script_prints_the_figures(part_c, figure):
    assert figure in part_c


@pytest.mark.parametrize("figure", ["−0.98", "0.2729", "−0.3092", "1.8636", "−1.6364", "0.4949", "1.2987", "0.7033",
                                    "0.1988", "0.7500", "0.1978", "0.4011", "10.2546", "£1.80", "£1.20", "2.6645",
                                    "3.6645", "−0.0202"])
@needs_book
def test_solutions_quote_the_computed_figures(figure):
    assert figure in TEXT


def test_hand_steps_of_c1_and_c2_are_right():
    import math
    assert f"{math.exp(0.98):.4f}" == "2.6645"
    assert f"{-0.3092 * 0.8 + 1.8636 - 1.6364:.4f}" == "-0.0202"


def test_faulty_log_shows_the_three_faults():
    out = run(GA / "faulty_shop_log.py")
    assert '[step 3] tool get_price({"item": "butter"}) -> {"error": "unknown item \'butter\'"}' in out
    assert '[step 5] tool multiply({"a": 2.1, "b": 2.75}) -> {"result": 5.78}' in out
    assert '[step 6] tool add({"a": 5.78, "b": 1.5}) -> {"result": 7.28}' in out
    assert len(re.findall(r'tool gbp_to_eur\(\{"amount": 7.28\}\)', out)) == 6
    assert "[stop] step limit of 12 reached without a final answer" in out
    correct = run(GA / "faulty_shop_log.py", "--correct")
    assert "4.85 x 1.15 = 5.58 EUR" in correct
    assert "[step" not in correct


def grade(path):
    out = run(GA / "grade_library.py", path)
    return int(re.search(r"Part F score: (\d+) / 15", out).group(1)), out


def test_reference_library_agent_scores_15():
    assert grade(REPO / "solutions" / "vol1" / "global_assessment" / "library_agent.py")[0] == 15


def test_untouched_starter_scores_0_with_reread_pointers():
    score, out = grade(GA / "library_starter.py")
    assert score == 0 and "reread chapter 29" in out


def test_agent_without_the_maximum_loses_three_points():
    src = (REPO / "solutions" / "vol1" / "global_assessment" / "library_agent.py").read_text(encoding="utf-8")
    broken = src.replace('min(days * RULES["fine_per_day_gbp"], RULES["maximum_fine_gbp"])',
                         'days * RULES["fine_per_day_gbp"]')
    assert broken != src
    # The agent finds the repository from its own location, so the broken copy must live inside it.
    path = GA / f"_test_broken_library_agent_{os.getpid()}.py"     # a unique name: no stale cache, no clash
    path.write_text(broken, encoding="utf-8")
    try:
        assert grade(path)[0] == 12
    finally:
        path.unlink()


@needs_book
def test_points_add_up_to_100():
    table = re.search(r"\| A \| Vocabulary.*?\*\*Total\*\* \| \| \*\*100\*\*", TEXT, re.S).group(0)
    points = [int(p) for p in re.findall(r"\| (\d+) \|\n", table)]
    assert sum(points) == 100


@needs_book
def test_vocabulary_answers_are_a_permutation():
    letters = re.findall(r"\| \d+ [A-Za-z -]+ \| ([a-t]) ", TEXT)
    assert sorted(letters) == sorted("abcdefghijklmnopqrst")


@pytest.mark.parametrize("section, figures", [
    ("percent", ["= 1.32%", "= 85.00%", "= -4.55%"]),
    ("weighted", ["Simple average of the 5 rates: 9.7080%", "Weighted average (by balance): 9.9806%", "pool: 9.31%"]),
    ("probability", ["P(bad) = 146 / 4,999 = 0.0292", "= 99 / 575 = 0.1722", "= 47 / 4,424 = 0.0106"]),
    ("spread", ["mean = 3811 / 5 = 762.2", "standard deviation = 94.48"]),
    ("vectors", ["W x = [1.0, 3.0]", "A B = [[4, 6], [1, 3]]", "= 0.7071"]),
])
def test_maths_examples(section, figures):
    out = run(REPO / "python" / "vol1" / "appendix_maths" / "maths_examples.py", section)
    for f in figures:
        assert f in out


@needs_book
def test_maths_prose_figures():
    assert "−4.77%" in MATHS and "9.98%" in MATHS and "9.71%" in MATHS and "16.2" in MATHS
    assert f"{(49151532.52 - 51494567.89) / 49151532.52:.2%}" == "-4.77%"
    assert f"{0.1722 / 0.0106:.1f}" == "16.2"
    assert f"{25734.76 / 27230:.4f}" == "0.9451"
