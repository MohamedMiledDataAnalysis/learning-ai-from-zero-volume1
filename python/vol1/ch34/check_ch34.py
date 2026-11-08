"""Practical task of chapter 34: Workflow cost of 2 loaves of bread and 1 cheese, in euros.

    python python/vol1/ch34/check_ch34.py <your answer>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from part6_checker import grade  # noqa: E402,F401

from shop_tools import add, gbp_to_eur, get_price, multiply
pounds = add(multiply(2, get_price('loaf of bread')['price_gbp'])['result'], get_price('cheese')['price_gbp'])['result']
expected = gbp_to_eur(pounds)['amount_eur']

grade("Workflow cost of 2 loaves of bread and 1 cheese, in euros", expected, "§ 34.2")
