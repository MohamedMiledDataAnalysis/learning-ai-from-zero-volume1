"""Practical task (chapter 19): a phone call now costs 60 instead of 10. Using value iteration
(exact_values), what is the best action for a loan 2 instalments in arrears? Answer nothing, reminder or call."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from part3_checker import check
from ch19 import collections_q_learning as cq

cq.COST["call"] = -60
check(cq.ACTIONS[int(cq.exact_values()[1].argmax())], 0, "§ 19.4")
