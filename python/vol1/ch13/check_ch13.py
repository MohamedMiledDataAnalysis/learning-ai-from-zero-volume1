"""Practical task (chapter 13): change rule R6 so the original LTV must be 95% or less.
How many rows of the received tape pass all six rules?"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import pandas as pd
from part3_checker import check
from ch13 import eligibility_rules as er

tape = pd.read_csv("data/loan_tape_cutoff.csv", keep_default_na=False)
rules = er.RULES[:5] + [("R6", lambda loan: loan["ltv_original_pct"] <= 95)]
expected = sum(all(test(loan) for _, test in rules) for _, loan in tape.iterrows())
check(expected, 0, "§ 13.2")
